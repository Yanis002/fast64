from ....utility import PluginError, toAlnum
from ...model.classes import OOTModel
from ...panel.properties.general.actor import OOTActorHeaderProperty
from .export import OOTCommonCommands, CullGroup
from .actor import OOTActor

from ....f3d.f3d_gbi import (
    SPDisplayList,
    SPEndDisplayList,
    GfxListTag,
    GfxList,
    DLFormat,
)


class OOTDLGroup:
    def __init__(self, name: str, DLFormat: DLFormat):
        self.opaque: GfxList = None
        self.transparent: GfxList = None
        self.DLFormat = DLFormat
        self.name = toAlnum(name)

    def addDLCall(self, displayList: GfxList, drawLayer: str):
        if drawLayer == "Opaque":
            if self.opaque is None:
                self.opaque = GfxList(f"{self.name}_opaque", GfxListTag.Draw, self.DLFormat)
            self.opaque.commands.append(SPDisplayList(displayList))
        elif drawLayer == "Transparent":
            if self.transparent is None:
                self.transparent = GfxList(f"{self.name}_transparent", GfxListTag.Draw, self.DLFormat)
            self.transparent.commands.append(SPDisplayList(displayList))
        else:
            raise PluginError(f"Unhandled draw layer: {drawLayer}")

    def terminateDLs(self):
        if self.opaque is not None:
            self.opaque.commands.append(SPEndDisplayList())

        if self.transparent is not None:
            self.transparent.commands.append(SPEndDisplayList())

    def createDLs(self):
        if self.opaque is None:
            self.opaque = GfxList(f"{self.name}_opaque", GfxListTag.Draw, self.DLFormat)
        if self.transparent is None:
            self.transparent = GfxList(f"{self.name}_transparent", GfxListTag.Draw, self.DLFormat)

    def isEmpty(self):
        return self.opaque is None and self.transparent is None


class OOTRoomMeshGroup:
    def __init__(self, cullGroup: CullGroup, dlFormat: DLFormat, roomName: str, entryIndex: int):
        self.cullGroup = cullGroup
        self.roomName = roomName
        self.entryIndex = entryIndex

        self.DLGroup = OOTDLGroup(self.getEntryName(), dlFormat)

    def getEntryName(self):
        return f"{self.roomName}_entry_{self.entryIndex}"


class OOTRoomMesh:
    def __init__(self, roomName: str, roomShape: str, model: OOTModel):
        self.roomName = roomName
        self.roomShape = roomShape
        self.meshEntries: list[OOTRoomMeshGroup] = []
        self.model = model

    def terminateDLs(self):
        for entry in self.meshEntries:
            entry.DLGroup.terminateDLs()

    def getHeaderName(self):
        return f"{self.roomName}_shapeHeader"

    def getEntriesName(self):
        entryName = "shapeDListEntry" if self.roomShape == "ROOM_SHAPE_TYPE_NORMAL" else "shapeCullableEntry"
        return f"{self.roomName}_{entryName}"

    def newMeshGroup(self, cullGroup: CullGroup):
        meshGroup = OOTRoomMeshGroup(cullGroup, self.model.DLFormat, self.roomName, len(self.meshEntries))
        self.meshEntries.append(meshGroup)
        return meshGroup

    def removeUnusedEntries(self):
        newList = []
        for meshEntry in self.meshEntries:
            if not meshEntry.DLGroup.isEmpty():
                newList.append(meshEntry)
        self.meshEntries = newList


class OOTRoom(OOTCommonCommands):
    def __init__(self, index: int, name: str, model: OOTModel, roomShape: str):
        self.ownerName = toAlnum(name)
        self.index = index
        self.mesh = OOTRoomMesh(self.getRoomName(), roomShape, model)

        # Room behaviour
        self.roomBehaviour = str()
        self.disableWarpSongs = False
        self.showInvisibleActors = False
        self.linkIdleMode = str()
        self.linkIdleModeCustom = str()

        self.customBehaviourX = None  # unused
        self.customBehaviourY = None  # unused

        # Wind
        self.setWind = False
        self.windVector = [0, 0, 0]  # direction (X, Y, Z)
        self.windStrength = 0  # based on wind vector

        # Time
        self.timeHours = 0
        self.timeMinutes = 0
        self.timeSpeed = 1

        # Skybox
        self.disableSkybox = False
        self.disableSunMoon = False

        # Echo
        self.echo = 0x00  # between 0 and 127 (?)

        # Other
        self.objectIDList: list[str] = []
        self.actorList: list[OOTActor] = []  # filled in ``add_actor()`` (called by ``processRoomContent``)

        # Alternate Layers
        self.childNightHeader = None
        self.adultDayHeader = None
        self.adultNightHeader = None
        self.cutsceneHeaders: list["OOTRoom"] = []
        self.layerIndex: int = -1  # intended value to see if this was set or not
        self.altLayers = ["childDayHeader", "childNightHeader", "adultDayHeader", "adultNightHeader"]

    def addActor(self, actor: OOTActor, layerProp: OOTActorHeaderProperty, objName: str):
        """Adds an OOTActor in the actor list to export in C code"""
        # add actors to export in the room's actor list for every layers
        if layerProp.sceneSetupPreset != "Custom":
            self.actorList.append(actor)
            for i, layer in enumerate(self.altLayers):
                if i > 0:
                    altLayer = getattr(self, layer)
                    if altLayer is not None:
                        actorList: list[OOTActor] = getattr(altLayer, "actorList")
                        actorList.append(actor)

            # avoid adding actors to cutscene layers if "non-cutscene layers" is selected
            if layerProp.sceneSetupPreset == "All Scene Setups" and self.layerIndex > 3:
                self.actorList.append(actor)

        elif layerProp.sceneSetupPreset == "Custom":
            for i, layer in enumerate(self.altLayers):
                if self.layerIndex != -1:
                    if getattr(layerProp, layer) and self.layerIndex == i:
                        self.actorList.append(actor)
                else:
                    raise PluginError("ERROR: Value Error for Layer Index!")

            for csLayer in layerProp.cutsceneHeaders:
                # csLayer type -> OOTActorHeaderItemProperty
                if self.layerIndex < (len(layerProp.cutsceneHeaders) + 1) + 4:
                    if self.layerIndex == csLayer.headerIndex:
                        actorList: list[OOTActor] = getattr(self, "actorList")
                        actorList.append(actor)
                else:
                    raise PluginError(
                        f"Object: '{objName}' uses a cutscene layer index that is outside "
                        + "the range of the current number of cutscene layers."
                    )
        else:
            raise PluginError(f"Unhandled scene setup preset: {layerProp.sceneSetupPreset}")

    def newAltLayer(self, name: str, layerIndex: int):
        newLayer = OOTRoom(self.index, name, self.mesh.model, self.mesh.roomShape)
        newLayer.mesh = self.mesh
        newLayer.layerIndex = layerIndex
        return newLayer

    def getRoomName(self):
        return f"{self.ownerName}_room_{self.index}"

    def getRoomLayerName(self, headerIndex: int):
        """Returns the room's name with the current layer index in it"""
        return f"{self.getRoomName()}_header{headerIndex:02}"

    def getObjectListName(self, headerIndex: int):
        return f"{self.getRoomLayerName(headerIndex)}_objectList"

    def getActorListName(self, headerIndex: int):
        return f"{self.getRoomLayerName(headerIndex)}_actorList"

    def getAltLayersListName(self):
        return f"{self.getRoomName()}_alternateLayers"

    def hasAltLayers(self):
        return not (
            self.childNightHeader == None
            and self.adultDayHeader == None
            and self.adultNightHeader == None
            and len(self.cutsceneHeaders) == 0
        )
