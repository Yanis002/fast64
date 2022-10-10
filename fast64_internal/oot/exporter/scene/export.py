import bpy
from bpy.types import Object, Camera, Curve
from math import radians, degrees
from mathutils import Quaternion, Matrix
from ....f3d.f3d_gbi import DLFormat
from ....utility import PluginError, unhideAllAndGetHiddenList, hideObjsInList
from ...collision.classes import OOTCameraPositionProperty
from ..collision import exportCollisionCommon
from ...model import OOTModel
from ..utility import getConvertedTransformWithOrientation
from ..cutscene import convertCutsceneData, processCutscene
from ..room import processRoom
from ..classes.collision import OOTCameraData, OOTCameraPosData
from ..classes.scene import OOTScene, OOTExit, OOTLight, OOTPath
from .data import decomp_compat_map_CameraSType

from ...scene.classes import (
    OOTAlternateSceneHeaderProperty,
    OOTSceneHeaderProperty,
    OOTSceneProperties,
    OOTLightGroupProperty,
)

from ...oot_utility import (
    OOTObjectCategorizer,
    getCustomProperty,
    ootDuplicateHierarchy,
    ootCleanupScene,
    getCustomProperty,
)


def assertCurveValid(obj: Object):
    curve = obj.data

    if not isinstance(curve, Curve) or curve.splines[0].type != "NURBS":
        # Curve was likely not intended to be exported
        return False

    if len(curve.splines) != 1:
        # Curve was intended to be exported but has multiple disconnected segments
        raise PluginError("Exported curves should have only one single segment, found " + str(len(curve.splines)))

    return True


def convertCamPosData(inCamObj: Object, outScene: OOTScene, inSceneObj: Object, transformMatrix: Matrix):
    # Camera faces opposite direction
    orientation = Quaternion((0, 1, 0), radians(180.0))

    translation, rotation, scale, orientedRotation = getConvertedTransformWithOrientation(
        transformMatrix, inSceneObj, inCamObj, orientation
    )

    camPosProp: OOTCameraPositionProperty = inCamObj.ootCameraPositionProperty

    # TODO: FOV conversion?
    if camPosProp.index in outScene.collision.cameraData.camPosDict:
        raise PluginError(f"Error: Repeated camera position index: {camPosProp.index}")

    if camPosProp.camSType == "Custom":
        camSType = camPosProp.camSTypeCustom
    else:
        camSType = decomp_compat_map_CameraSType.get(camPosProp.camSType, camPosProp.camSType)

    outScene.collision.cameraData.camPosDict[camPosProp.index] = OOTCameraPosData(
        camSType,
        camPosProp.hasPositionData,
        translation,
        rotation,
        round(degrees(inCamObj.data.angle)),
        camPosProp.jfifID,
    )


def ootConvertPath(name: str, index: int, obj: Object, transformMatrix: Matrix):
    path = OOTPath(name, index)

    for point in obj.data.splines[0].points:
        position = transformMatrix @ point.co
        path.points.append(position)

    return path


def convertPathData(obj: Object, outScene: OOTScene, inSceneObj: Object, sceneName: str, transformMatrix: Matrix):
    relativeTransform = transformMatrix @ inSceneObj.matrix_world.inverted() @ obj.matrix_world
    index: int = obj.ootSplineProperty.index

    if not index in outScene.pathList:
        outScene.pathList[index] = ootConvertPath(sceneName, index, obj, relativeTransform)
    else:
        raise PluginError(f"ERROR: Object: '{obj.name}' has a repeated spline index: {index}")


def convertSceneLayer(
    outScene: OOTScene,
    inSceneProps: OOTSceneProperties,
    inSceneLayerProp: OOTSceneHeaderProperty,
):
    # Dummy Room List
    outScene.write_dummy_room_list = inSceneProps.write_dummy_room_list

    # Draw Config
    outScene.sceneTableEntry.drawConfig = inSceneLayerProp.sceneTableEntry.drawConfig

    # Global Scene Object
    outScene.globalObject = getCustomProperty(inSceneLayerProp, "globalObject")

    # Navi Hints
    outScene.naviCup = getCustomProperty(inSceneLayerProp, "naviCup")

    # Skybox
    outScene.skyboxID = getCustomProperty(inSceneLayerProp, "skyboxID")
    outScene.skyboxCloudiness = getCustomProperty(inSceneLayerProp, "skyboxCloudiness")
    outScene.skyboxLighting = getCustomProperty(inSceneLayerProp, "skyboxLighting")

    # Lighting
    outScene.lightMode = inSceneLayerProp.skyboxLighting

    if inSceneLayerProp.skyboxLighting == "0x00":
        # Time of Day
        todLights: OOTLightGroupProperty = inSceneLayerProp.timeOfDayLights
        for lightType in ["dawn", "day", "dusk", "night"]:
            outScene.lights.append(OOTLight(getattr(todLights, lightType)))
    else:
        # Indoor or Custom
        for lightProp in inSceneLayerProp.lightList:
            outScene.lights.append(OOTLight(lightProp))

    # Map Location
    outScene.mapLocation = getCustomProperty(inSceneLayerProp, "mapLocation")

    # Camera Mode
    outScene.cameraMode = getCustomProperty(inSceneLayerProp, "cameraMode")

    # Audio
    outScene.musicSeq = getCustomProperty(inSceneLayerProp, "musicSeq")
    outScene.nightSeq = getCustomProperty(inSceneLayerProp, "nightSeq")
    outScene.audioSessionPreset = getCustomProperty(inSceneLayerProp, "audioSessionPreset")

    # Exits
    for exitProp in inSceneLayerProp.exitList:
        outScene.exitList.append(OOTExit(exitProp))

    # Cutscenes
    outScene.writeCutscene = getCustomProperty(inSceneLayerProp, "writeCutscene")
    if outScene.writeCutscene:
        outScene.csWriteType = getattr(inSceneLayerProp, "csWriteType")
        if outScene.csWriteType == "Embedded":
            outScene.csEndFrame = getCustomProperty(inSceneLayerProp, "csEndFrame")
            outScene.csWriteTerminator = getCustomProperty(inSceneLayerProp, "csWriteTerminator")
            outScene.csTermIdx = getCustomProperty(inSceneLayerProp, "csTermIdx")
            outScene.csTermStart = getCustomProperty(inSceneLayerProp, "csTermStart")
            outScene.csTermEnd = getCustomProperty(inSceneLayerProp, "csTermEnd")
            convertCutsceneData(outScene, inSceneLayerProp)

        elif outScene.csWriteType == "Custom":
            outScene.csWriteCustom = getCustomProperty(inSceneLayerProp, "csWriteCustom")

        elif outScene.csWriteType == "Object":
            if inSceneLayerProp.csWriteObject is None:
                raise PluginError("No object selected for cutscene reference")
            elif inSceneLayerProp.csWriteObject.ootEmptyType != "Cutscene":
                raise PluginError("Object selected as cutscene is wrong type, must be empty with Cutscene type")
            elif inSceneLayerProp.csWriteObject.parent is not None:
                raise PluginError("Cutscene empty object should not be parented to anything")
            else:
                outScene.csWriteObject = processCutscene(inSceneLayerProp.csWriteObject)


def processScene(
    inSceneObj: Object,
    transformMatrix: Matrix,
    f3dType: str,
    isHWv1: bool,  # is hardware v1
    sceneName: str,
    dlFormat: DLFormat,
    convertTextureData: bool,
):
    if inSceneObj.data is not None or inSceneObj.ootEmptyType != "Scene":
        raise PluginError(f"ERROR: Object: '{inSceneObj.name}' is not an empty object with the 'Scene' type!")

    if bpy.context.scene.exportHiddenGeometry:
        hiddenObjs = unhideAllAndGetHiddenList(bpy.context.scene)

    # Don't remove ignore_render, as we want to reuse this for collision
    sceneObj, allObjs = ootDuplicateHierarchy(inSceneObj, None, True, OOTObjectCategorizer())

    if bpy.context.scene.exportHiddenGeometry:
        hideObjsInList(hiddenObjs)

    try:
        # Process the scene data
        outScene = OOTScene(sceneName, OOTModel(f3dType, isHWv1, sceneName + "_dl", dlFormat, None))

        inSceneLayerProp: OOTSceneHeaderProperty = sceneObj.ootSceneHeader
        inSceneProps: OOTSceneProperties = sceneObj.fast64.oot.scene
        convertSceneLayer(outScene, inSceneProps, inSceneLayerProp)

        # Process the scene's alternate layers, if used
        altSceneLayers: OOTAlternateSceneHeaderProperty = sceneObj.ootAlternateSceneHeaders
        if altSceneLayers is not None:
            for ec in inSceneLayerProp.extraCutscenes:
                outScene.extraCutscenes.append(processCutscene(ec.csObject))

            outScene.collision.cameraData = OOTCameraData(outScene.name)

            for i, altLayer in enumerate(outScene.altLayers):
                if i > 0:
                    curLayerProp = getattr(altSceneLayers, altLayer)
                    if not curLayerProp.usePreviousHeader:
                        setattr(outScene, altLayer, outScene.newAltLayer(outScene.name))
                        convertSceneLayer(getattr(outScene, altLayer), inSceneProps, curLayerProp)

            for csLayer in altSceneLayers.cutsceneHeaders:
                curLayer = outScene.newAltLayer(outScene.name)
                convertSceneLayer(curLayer, inSceneProps, csLayer)
                outScene.cutsceneHeaders.append(curLayer)

        elif len(inSceneLayerProp.extraCutscenes) > 0:
            raise PluginError(
                "Extra cutscenes (not in any header) only belong in the main scene, not alternate headers"
            )

        # Process the rooms
        processedRooms = set[int]()
        roomQueue = []

        for obj in sceneObj.children_recursive:
            if obj.data is None and obj.ootEmptyType == "Room":
                if not obj in roomQueue:
                    roomQueue.append(obj)
            elif isinstance(obj.data, Camera):
                convertCamPosData(obj, outScene, sceneObj, transformMatrix)
            elif isinstance(obj.data, Curve) and assertCurveValid(obj):
                convertPathData(obj, outScene, sceneObj, sceneName, transformMatrix)

        if len(roomQueue) > 0:
            for roomObj in roomQueue:
                processRoom(outScene, sceneObj, roomObj, processedRooms, sceneName, transformMatrix, convertTextureData)
        else:
            raise PluginError("The scene has no child empties with the 'Room' empty type.")

        outScene.validateIndices()
        outScene.entranceList = sorted(outScene.entranceList, key=lambda x: x.startPositionIndex)
        exportCollisionCommon(outScene.collision, sceneObj, transformMatrix, True)

        ootCleanupScene(inSceneObj, allObjs)

    except Exception as e:
        ootCleanupScene(inSceneObj, allObjs)
        raise Exception(str(e))

    return outScene
