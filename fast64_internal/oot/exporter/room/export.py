from math import radians
from mathutils import Vector, Matrix, Quaternion
from bpy.types import Object
from ....utility import PluginError, checkIdentityRotation, normToSigned8Vector
from ...oot_utility import CullGroup, getCustomProperty
from ...oot_collision_classes import OOTWaterBox
from ...room.classes import OOTAlternateRoomHeaderProperty, OOTRoomHeaderProperty
from ...actor.classes import OOTActorProperty, OOTTransitionActorProperty, OOTEntranceProperty
from ..classes.scene import OOTScene
from ..classes.room import OOTRoom
from ..classes.actor import OOTActor, OOTTransitionActor, OOTEntrance
from ..utility import getConvertedTransformWithOrientation, ootProcessMesh


def getConvertedTransform(transformMatrix: Matrix, sceneObj: Object, obj: Object, handleOrientation: bool):
    # Hacky solution to handle Z-up to Y-up conversion
    # We cannot apply rotation to empty, as that modifies scale
    if handleOrientation:
        orientation = Quaternion((1, 0, 0), radians(90.0))
    else:
        orientation = Matrix.Identity(4)
    return getConvertedTransformWithOrientation(transformMatrix, sceneObj, obj, orientation)


def processRoomContent(
    outScene: OOTScene,
    outRoom: OOTRoom,
    inRoomObj: Object,
    positions: list[int],
    rotations: list[int],
):
    if inRoomObj.ootEmptyType == "Actor":
        actorProp: OOTActorProperty = inRoomObj.ootActorProperty
        outRoom.addActor(
            OOTActor(
                getCustomProperty(actorProp, "actorID"),
                positions,
                [f"0x{rot:04X}" for rot in rotations]
                if not actorProp.rotOverride
                else [actorProp.rotOverrideX, actorProp.rotOverrideY, actorProp.rotOverrideZ],
                actorProp.actorParam,
            ),
            actorProp.headerSettings,
            inRoomObj.name,
        )
    elif inRoomObj.ootEmptyType == "Transition Actor":
        transActorProp: OOTTransitionActorProperty = inRoomObj.ootTransitionActorProperty
        outScene.addActor(
            OOTTransitionActor(
                getCustomProperty(transActorProp.actor, "actorID"),
                outRoom.index,
                transActorProp.roomIndex,
                getCustomProperty(transActorProp, "cameraTransitionFront"),
                getCustomProperty(transActorProp, "cameraTransitionBack"),
                positions,
                rotations[1],  # TODO: Correct axis?
                transActorProp.actor.actorParam,
            ),
            transActorProp.actor.headerSettings,
            inRoomObj.name,
            "transitionActorList",
        )
    elif inRoomObj.ootEmptyType == "Entrance":
        entranceProp: OOTEntranceProperty = inRoomObj.ootEntranceProperty
        spawnIndex = entranceProp.spawnIndex
        outScene.addActor(
            OOTEntrance(outRoom.index, spawnIndex), entranceProp.actor.headerSettings, inRoomObj.name, "entranceList"
        )
        outScene.addStartPosition(
            spawnIndex,
            OOTActor(
                "ACTOR_PLAYER" if not entranceProp.customActor else entranceProp.actor.actorIDCustom,
                positions,
                [f"0x{rot:04X}" for rot in rotations],
                entranceProp.actor.actorParam,
            ),
            entranceProp.actor.headerSettings,
            inRoomObj.name,
        )


def processWaterBox(sceneObj: Object, obj: Object, transformMatrix: Matrix, scene: OOTScene, roomIndex: int):
    translation, rotation, scale, orientedRotation = getConvertedTransform(transformMatrix, sceneObj, obj, True)

    checkIdentityRotation(obj, orientedRotation, False)
    waterBoxProp = obj.ootWaterBoxProperty
    scene.collision.waterBoxes.append(
        OOTWaterBox(
            roomIndex,
            getCustomProperty(waterBoxProp, "lighting"),
            getCustomProperty(waterBoxProp, "camera"),
            translation,
            scale,
            obj.empty_display_size,
        )
    )


def convertRoomLayer(
    outScene: OOTScene,
    outRoom: OOTRoom,
    inRoomLayer: OOTRoomHeaderProperty,
    inSceneObj: Object,
    inRoomObj: Object,
    transformMatrix: Matrix,
    processSceneActors: bool,
    processedWaterBoxes: set,
):
    outRoom.index = inRoomLayer.roomIndex

    # Room Behavior
    outRoom.roomBehaviour = getCustomProperty(inRoomLayer, "roomBehaviour")
    outRoom.disableWarpSongs = inRoomLayer.disableWarpSongs
    outRoom.showInvisibleActors = inRoomLayer.showInvisibleActors

    # Room heat behavior is active if the idle mode is 0x03
    outRoom.linkIdleMode = getCustomProperty(inRoomLayer, "linkIdleMode") if not inRoomLayer.roomIsHot else "0x03"
    outRoom.linkIdleModeCustom = inRoomLayer.linkIdleModeCustom

    # Wind
    outRoom.setWind = inRoomLayer.setWind
    outRoom.windVector = normToSigned8Vector(Vector(inRoomLayer.windVector).normalized())
    outRoom.windStrength = int(0xFF * max(Vector(inRoomLayer.windVector).length, 1))

    # Time
    outRoom.timeHours = inRoomLayer.timeHours if not inRoomLayer.leaveTimeUnchanged else "255"
    outRoom.timeMinutes = inRoomLayer.timeMinutes if not inRoomLayer.leaveTimeUnchanged else "255"
    outRoom.timeSpeed = int(inRoomLayer.timeSpeed * 10)

    # Sky Settings
    outRoom.disableSkybox = inRoomLayer.disableSkybox
    outRoom.disableSunMoon = inRoomLayer.disableSunMoon

    # Other
    outRoom.echo = inRoomLayer.echo
    outRoom.objectIDList.extend([getCustomProperty(item, "objectID") for item in inRoomLayer.objectList])
    if len(outRoom.objectIDList) > 15:
        raise PluginError("Error: A scene can only have a maximum of 15 objects (OOT, not blender objects).")

    emptyTypes = ["Actor", "Water Box"]
    if processSceneActors:
        emptyTypes.extend(["Transition Actor", "Entrance"])

    # Room Content
    for childObj in inRoomObj.children_recursive:
        positions, rotations, scale, orientedRotation = getConvertedTransform(
            transformMatrix, inSceneObj, childObj, True
        )
        if childObj.data is None and childObj.ootEmptyType in emptyTypes:
            if childObj.ootEmptyType == "Water Box":
                if not childObj in processedWaterBoxes:
                    roomIndex = 0x3F if childObj.ootWaterBoxProperty.isGlobal else inRoomObj.ootRoomHeader.roomIndex
                    processWaterBox(inSceneObj, childObj, transformMatrix, outScene, roomIndex)
                    processedWaterBoxes.add(childObj)
            else:
                processRoomContent(outScene, outRoom, childObj, positions, rotations)


def processRoom(
    outScene: OOTScene,
    inSceneObj: Object,
    inRoomObj: Object,
    processedRooms: set[int],
    sceneName: str,
    transformMatrix: Matrix,
    convertTextureData: bool,
):
    roomIndex: int = inRoomObj.ootRoomHeader.roomIndex
    if not roomIndex in processedRooms:
        processedRooms.add(roomIndex)
    else:
        raise PluginError(f"ERROR: Room index: '{roomIndex}' is used more than once.")

    outRoom = outScene.newRoom(roomIndex, sceneName, inRoomObj.ootRoomHeader.roomShape)
    outRoom.layerIndex = 0

    positions, rotations, scale, orientedRotation = getConvertedTransform(transformMatrix, inSceneObj, inRoomObj, True)
    processedWaterBoxes = set()
    convertRoomLayer(
        outScene,
        outRoom,
        inRoomObj.ootRoomHeader,
        inSceneObj,
        inRoomObj,
        transformMatrix,
        True,
        processedWaterBoxes,
    )

    altLayerProp: OOTAlternateRoomHeaderProperty = inRoomObj.ootAlternateRoomHeaders
    if altLayerProp is not None:
        for i, altLayer in enumerate(outRoom.altLayers):
            if i > 0:
                inRoomLayerProp: OOTRoomHeaderProperty = getattr(altLayerProp, altLayer)
                if not inRoomLayerProp.usePreviousHeader:
                    setattr(outRoom, altLayer, outRoom.newAltLayer(outRoom.ownerName, i))
                    convertRoomLayer(
                        outScene,
                        getattr(outRoom, altLayer),
                        inRoomLayerProp,
                        inSceneObj,
                        inRoomObj,
                        transformMatrix,
                        False,
                        processedWaterBoxes,
                    )

        for i, inCsLayerProp in enumerate(altLayerProp.cutsceneHeaders, 4):
            outCsLayer = outRoom.newAltLayer(outRoom.ownerName, i)
            outRoom.cutsceneHeaders.append(outCsLayer)
            convertRoomLayer(
                outScene,
                outCsLayer,
                inCsLayerProp,
                inSceneObj,
                inRoomObj,
                transformMatrix,
                False,
                processedWaterBoxes,
            )

    dlGroup = outRoom.mesh.newMeshGroup(
        CullGroup(positions, scale, inRoomObj.ootRoomHeader.defaultCullDistance)
    ).DLGroup
    ootProcessMesh(outRoom.mesh, dlGroup, inSceneObj, inRoomObj, transformMatrix, convertTextureData, None)
    outRoom.mesh.terminateDLs()
    outRoom.mesh.removeUnusedEntries()
