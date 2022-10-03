from mathutils import Vector
from bpy.types import Camera, Curve, Object
from ....utility import PluginError, normToSigned8Vector
from ...oot_utility import CullGroup, getCustomProperty
from ...oot_spline import assertCurveValid
from ...room.classes import OOTAlternateRoomHeaderProperty, OOTRoomHeaderProperty
from ...actor.classes import OOTActorProperty, OOTTransitionActorProperty, OOTEntranceProperty
from ..classes.scene import OOTScene
from ..classes.room import OOTRoom
from ..classes.actor import OOTActor, OOTTransitionActor, OOTEntrance
from ..utility import getConvertedTransform, ootProcessWaterBox, ootProcessMesh, readCamPos, readPathProp


def ootProcessEmpties(scene: OOTScene, room: OOTRoom, sceneObj: Object, obj: Object, transformMatrix):
    translation, rotation, scale, orientedRotation = getConvertedTransform(transformMatrix, sceneObj, obj, True)

    if obj.data is None:
        if obj.ootEmptyType == "Actor":
            actorProp: OOTActorProperty = obj.ootActorProperty
            room.addActor(
                OOTActor(
                    getCustomProperty(actorProp, "actorID"),
                    translation,
                    rotation,
                    actorProp.actorParam,
                    None
                    if not actorProp.rotOverride
                    else (actorProp.rotOverrideX, actorProp.rotOverrideY, actorProp.rotOverrideZ),
                ),
                actorProp.headerSettings,
                obj.name,
            )
        elif obj.ootEmptyType == "Transition Actor":
            transActorProp: OOTTransitionActorProperty = obj.ootTransitionActorProperty
            scene.addActor(
                OOTTransitionActor(
                    getCustomProperty(transActorProp.actor, "actorID"),
                    room.index,
                    transActorProp.roomIndex,
                    getCustomProperty(transActorProp, "cameraTransitionFront"),
                    getCustomProperty(transActorProp, "cameraTransitionBack"),
                    translation,
                    rotation[1],  # TODO: Correct axis?
                    transActorProp.actor.actorParam,
                ),
                transActorProp.actor.headerSettings,
                obj.name,
                "transitionActorList",
            )
        elif obj.ootEmptyType == "Entrance":
            entranceProp: OOTEntranceProperty = obj.ootEntranceProperty
            spawnIndex = entranceProp.spawnIndex
            scene.addActor(
                OOTEntrance(room.index, spawnIndex), entranceProp.actor.headerSettings, obj.name, "entranceList"
            )
            scene.addStartPosition(
                spawnIndex,
                OOTActor(
                    "ACTOR_PLAYER" if not entranceProp.customActor else entranceProp.actor.actorIDCustom,
                    translation,
                    rotation,
                    entranceProp.actor.actorParam,
                    None,
                ),
                entranceProp.actor.headerSettings,
                obj.name,
            )
        elif obj.ootEmptyType == "Water Box":
            ootProcessWaterBox(sceneObj, obj, transformMatrix, scene, room.roomIndex)
    elif isinstance(obj.data, Camera):
        camPosProp = obj.ootCameraPositionProperty
        readCamPos(camPosProp, obj, scene, sceneObj, transformMatrix)
    elif isinstance(obj.data, Curve) and assertCurveValid(obj):
        readPathProp(obj.ootSplineProperty, obj, scene, sceneObj, scene.name, transformMatrix)

    for childObj in obj.children:
        ootProcessEmpties(scene, room, sceneObj, childObj, transformMatrix)


def readRoomData(
    room: OOTRoom, roomHeader: OOTRoomHeaderProperty, alternateRoomHeaders: OOTAlternateRoomHeaderProperty
):
    room.roomIndex = roomHeader.roomIndex
    room.roomBehaviour = getCustomProperty(roomHeader, "roomBehaviour")
    room.disableWarpSongs = roomHeader.disableWarpSongs
    room.showInvisibleActors = roomHeader.showInvisibleActors
    room.linkIdleMode = getCustomProperty(roomHeader, "linkIdleMode")
    room.linkIdleModeCustom = roomHeader.linkIdleModeCustom
    room.setWind = roomHeader.setWind
    room.windVector = normToSigned8Vector(Vector(roomHeader.windVector).normalized())
    room.windStrength = int(0xFF * max(Vector(roomHeader.windVector).length, 1))
    if roomHeader.leaveTimeUnchanged:
        room.timeHours = "0xFF"
        room.timeMinutes = "0xFF"
    else:
        room.timeHours = roomHeader.timeHours
        room.timeMinutes = roomHeader.timeMinutes
    room.timeSpeed = max(-128, min(127, int(round(roomHeader.timeSpeed * 0xA))))
    room.disableSkybox = roomHeader.disableSkybox
    room.disableSunMoon = roomHeader.disableSunMoon
    room.echo = roomHeader.echo
    room.objectIDList.extend([getCustomProperty(item, "objectID") for item in roomHeader.objectList])
    if len(room.objectIDList) > 15:
        raise PluginError("Error: A scene can only have a maximum of 15 objects (OOT, not blender objects).")

    if alternateRoomHeaders is not None:
        if not alternateRoomHeaders.childNightHeader.usePreviousHeader:
            room.childNightHeader = room.getAlternateHeaderRoom(room.ownerName)
            readRoomData(room.childNightHeader, alternateRoomHeaders.childNightHeader, None)

        if not alternateRoomHeaders.adultDayHeader.usePreviousHeader:
            room.adultDayHeader = room.getAlternateHeaderRoom(room.ownerName)
            readRoomData(room.adultDayHeader, alternateRoomHeaders.adultDayHeader, None)

        if not alternateRoomHeaders.adultNightHeader.usePreviousHeader:
            room.adultNightHeader = room.getAlternateHeaderRoom(room.ownerName)
            readRoomData(room.adultNightHeader, alternateRoomHeaders.adultNightHeader, None)

        for i in range(len(alternateRoomHeaders.cutsceneHeaders)):
            cutsceneHeaderProp = alternateRoomHeaders.cutsceneHeaders[i]
            cutsceneHeader = room.getAlternateHeaderRoom(room.ownerName)
            readRoomData(cutsceneHeader, cutsceneHeaderProp, None)
            room.cutsceneHeaders.append(cutsceneHeader)


def processRoom(
    scene: OOTScene,
    sceneObj: Object,
    roomObj: Object,
    processedRooms: set[int],
    sceneName: str,
    transformMatrix,
    convertTextureData: bool,
):
    roomIndex: int = roomObj.ootRoomHeader.roomIndex
    translation, rotation, scale, orientedRotation = getConvertedTransform(transformMatrix, sceneObj, roomObj, True)

    if roomIndex in processedRooms:
        raise PluginError("Error: room index " + str(roomIndex) + " is used more than once.")

    processedRooms.add(roomIndex)

    room = scene.addRoom(roomIndex, sceneName, roomObj.ootRoomHeader.roomShape)
    readRoomData(room, roomObj.ootRoomHeader, roomObj.ootAlternateRoomHeaders)

    DLGroup = room.mesh.addMeshGroup(CullGroup(translation, scale, roomObj.ootRoomHeader.defaultCullDistance)).DLGroup

    ootProcessMesh(room.mesh, DLGroup, sceneObj, roomObj, transformMatrix, convertTextureData, None)
    room.mesh.terminateDLs()
    room.mesh.removeUnusedEntries()
    ootProcessEmpties(scene, room, sceneObj, roomObj, transformMatrix)
