from ....utility import PluginError, toAlnum, exportColor, ootGetBaseOrCustomLight
from ...oot_collision_classes import OOTCollision
from ...oot_model_classes import OOTModel
from ...oot_spline import OOTPath
from ...actor.classes import OOTActorHeaderProperty
from ...scene.classes import OOTExitProperty, OOTLightProperty
from .actor import OOTActor, OOTTransitionActor, OOTEntrance


class OOTExit:
    def __init__(self, exitProp: OOTExitProperty):
        if exitProp.exitIndex == "Custom":
            self.index = exitProp.exitIndexCustom
        else:
            raise PluginError("Exit index enums not implemented yet.")


class OOTLight:
    def __init__(self, lightProp: OOTLightProperty):
        self.ambient = exportColor(lightProp.ambient)
        self.diffuse0, self.diffuseDir0 = ootGetBaseOrCustomLight(lightProp, 0, True, True)
        self.diffuse1, self.diffuseDir1 = ootGetBaseOrCustomLight(lightProp, 1, True, True)
        self.fogColor = exportColor(lightProp.fogColor)
        self.fogNear = lightProp.fogNear
        self.transitionSpeed = lightProp.transitionSpeed
        self.fogFar = lightProp.fogFar

    def getBlendFogShort(self):
        return f"(({self.transitionSpeed} << 10) | {self.fogNear})"


class OOTSceneTableEntry:
    def __init__(self):
        self.drawConfig = 0


class OOTScene:
    def __init__(self, name: str, model: OOTModel):
        """Initialises the class"""
        self.name = toAlnum(name)
        self.write_dummy_room_list = False
        self.rooms = {}
        self.transitionActorList: list[OOTTransitionActor] = []
        self.entranceList: list[OOTEntrance] = []
        self.startPositions = {}
        self.lights: list[OOTLight] = []
        self.model = model
        self.collision = OOTCollision(self.name)

        self.globalObject = None
        self.naviCup = None

        # Skybox
        self.skyboxID = None
        self.skyboxCloudiness = None
        self.skyboxLighting = None
        self.lightMode = None

        # Camera
        self.mapLocation = None
        self.cameraMode = None

        self.musicSeq = None
        self.nightSeq = None

        self.childNightHeader = None
        self.adultDayHeader = None
        self.adultNightHeader = None
        self.cutsceneHeaders = []

        self.exitList = []
        self.pathList: dict[int, OOTPath] = {}
        self.cameraList = []

        self.writeCutscene = False
        self.csWriteType = "Embedded"
        self.csWriteCustom = ""
        self.csWriteObject = None
        self.csEndFrame = 100
        self.csWriteTerminator = False
        self.csTermIdx = 0
        self.csTermStart = 99
        self.csTermEnd = 100
        self.csLists = []
        self.extraCutscenes = []

        self.sceneTableEntry = OOTSceneTableEntry()

        self.altLayers = ["childDayHeader", "childNightHeader", "adultDayHeader", "adultNightHeader"]

    def addActor(
        self, actor: OOTTransitionActor | OOTEntrance, layerProp: OOTActorHeaderProperty, objName: str, listName: str
    ):
        """Adds an OOTTransitionActor or an OOTEntrance in the actor list to export in C code"""
        # add actors to export in the room's actor list for every layers
        if layerProp.sceneSetupPreset != "Custom":
            actorList = getattr(self, listName)
            actorList.append(actor)
            for i, layer in enumerate(self.altLayers):
                if i > 0:
                    altLayer = getattr(self, layer)
                    if altLayer is not None:
                        actorList = getattr(altLayer, listName)
                        actorList.append(actor)

            # avoid adding actors to cutscene layers if "non-cutscene layers" is selected
            if layerProp.sceneSetupPreset == "All Scene Setups":
                for csLayer in self.cutsceneHeaders:
                    actorList = getattr(csLayer, listName)
                    actorList.append(actor)

        elif layerProp.sceneSetupPreset == "Custom":
            for i, layer in enumerate(self.altLayers):
                curLayer = self if i == 0 else getattr(self, layer)
                actorLayer = getattr(layerProp, layer)
                if actorLayer and curLayer is not None:
                    actorList = getattr(curLayer, listName)
                    actorList.append(actor)

            for csLayer in layerProp.cutsceneHeaders:
                # csLayer type -> OOTActorHeaderItemProperty
                if csLayer.headerIndex < len(self.cutsceneHeaders) + 4:
                    layer = self.cutsceneHeaders[csLayer.headerIndex - 4]
                    actorList = getattr(layer, listName)
                    actorList.append(actor)
                else:
                    raise PluginError(
                        f"""
                            Object: '{objName}' uses a cutscene layer index that is outside
                            the range of the current number of cutscene layers.
                        """
                    )
        else:
            raise PluginError(f"Unhandled scene setup preset: {layerProp.sceneSetupPreset}")

    def addStartPosAtIndex(self, startPosDict: dict, index: int, actor: OOTActor):
        if index in startPosDict:
            raise PluginError("Error: Repeated start position spawn index: " + str(index))
        startPosDict[index] = actor

    def addStartPosition(self, index: int, actor: OOTActor, layerProp: OOTActorHeaderProperty, objName: str):
        if layerProp.sceneSetupPreset != "Custom":
            self.addStartPosAtIndex(self.startPositions, index, actor)

            for i, altLayer in enumerate(self.altLayers):
                if i > 0:
                    curLayer = getattr(self, altLayer)
                    if curLayer is not None:
                        self.addStartPosAtIndex(curLayer.startPositions, index, actor)

            if layerProp.sceneSetupPreset == "All Scene Setups":
                for cutsceneHeader in self.cutsceneHeaders:
                    self.addStartPosAtIndex(cutsceneHeader.startPositions, index, actor)
        else:
            for i, altLayer in enumerate(self.altLayers):
                actorLayer = getattr(layerProp, altLayer)
                curLayer = getattr(self, altLayer) if i > 0 else self
                if actorLayer and curLayer is not None:
                    self.addStartPosAtIndex(curLayer.startPositions, index, actor)

            for cutsceneHeader in layerProp.cutsceneHeaders:
                if cutsceneHeader.headerIndex < len(self.cutsceneHeaders) + 4:
                    self.addStartPosAtIndex(
                        self.cutsceneHeaders[cutsceneHeader.headerIndex - 4].startPositions, index, actor
                    )
                else:
                    raise PluginError(
                        f"""
                            Object: '{objName}' uses a cutscene layer index that is outside
                            the range of the current number of cutscene layers.
                        """
                    )

    def getAlternateHeaderScene(self, name: str):
        """Returns a new ``OOTScene()`` for the wanted header"""
        scene = OOTScene(name, self.model)
        scene.write_dummy_room_list = self.write_dummy_room_list
        scene.rooms = self.rooms
        scene.collision = self.collision
        scene.exitList = self.exitList
        scene.pathList = self.pathList
        scene.cameraList = self.cameraList
        return scene

    def sceneName(self):
        """Returns the scene's name"""
        return f"{self.name}_scene"

    def sceneHeaderName(self, headerIndex: int):
        """Returns the scene's name with the current header index in it"""
        return f"{self.sceneName()}_header{headerIndex:02}"

    def roomListName(self):
        return self.sceneName() + "_roomList"

    def entranceListName(self, headerIndex: int):
        return f"{self.sceneHeaderName(headerIndex)}_entranceList"

    def startPositionsName(self, headerIndex: int):
        return f"{self.sceneHeaderName(headerIndex)}_startPositionList"

    def exitListName(self, headerIndex: int):
        return f"{self.sceneHeaderName(headerIndex)}_exitList"

    def lightListName(self, headerIndex: int):
        return f"{self.sceneHeaderName(headerIndex)}_lightSettings"

    def transitionActorListName(self, headerIndex: int):
        return f"{self.sceneHeaderName(headerIndex)}_transitionActors"

    def pathListName(self):
        return self.sceneName() + "_pathway"

    def cameraListName(self):
        return self.sceneName() + "_cameraList"

    def cutsceneDataName(self, headerIndex: int):
        return f"{self.sceneHeaderName(headerIndex)}_cutscene"

    def alternateHeadersName(self):
        return self.sceneName() + "_alternateHeaders"

    def hasAlternateHeaders(self):
        return not (
            self.childNightHeader == None
            and self.adultDayHeader == None
            and self.adultNightHeader == None
            and len(self.cutsceneHeaders) == 0
        )

    def validateIndices(self):
        """Checks if the scene's indices are all correct"""
        self.collision.cameraData.validateCamPositions()  # ``collision.cameraData`` type: ``OOTCameraData``
        self.validateStartPositions()
        self.validateRoomIndices()
        self.validatePathIndices()

    def validateStartPositions(self):
        for index in range(len(self.startPositions)):
            if not (index in self.startPositions):
                raise PluginError(
                    "Error: Entrances (start positions) do not have a consecutive list of indices. "
                    + f"Missing index: {index}"
                )

    def validateRoomIndices(self):
        for index in range(len(self.rooms)):
            if not (index in self.rooms):
                raise PluginError(
                    f"Error: Room indices do not have a consecutive list of indices. Missing index: {index}"
                )

    def validatePathIndices(self):
        for index in range(len(self.pathList)):
            if not (index in self.pathList):
                raise PluginError(
                    f"Error: Path list does not have a consecutive list of indices. Missing index: {index}"
                )

    def addRoom(self, roomIndex: int, roomName: str, roomShape: str):
        """Adds a new room"""
        from .room import OOTRoom

        roomModel = self.model.addSubModel(
            OOTModel(self.model.f3d.F3D_VER, self.model.f3d._HW_VERSION_1, f"{roomName}_dl", self.model.DLFormat, None)
        )
        room = OOTRoom(roomIndex, roomName, roomModel, roomShape)

        if roomIndex in self.rooms:
            raise PluginError(f"Error: Repeated room index for room '{roomName}': {roomIndex}")

        self.rooms[roomIndex] = room
        return room
