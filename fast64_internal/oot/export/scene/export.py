import bpy
from bpy.types import Object
from ....f3d.f3d_gbi import DLFormat
from ....utility import PluginError, unhideAllAndGetHiddenList, hideObjsInList
from ...oot_spline import assertCurveValid
from ...oot_collision import exportCollisionCommon
from ...oot_collision_classes import OOTCameraData
from ...oot_model_classes import OOTModel
from ...scene.classes import OOTAlternateSceneHeaderProperty, OOTSceneHeaderProperty, OOTSceneProperties
from ..cutscene import readCutsceneData, convertCutsceneObject
from ..classes.scene import OOTScene
from ..room import processRoom
from ..utility import ootProcessWaterBox, readCamPos, readPathProp
from ..classes.scene import OOTExit, OOTLight

from ...oot_utility import (
    OOTObjectCategorizer,
    getCustomProperty,
    ootDuplicateHierarchy,
    ootCleanupScene,
    getCustomProperty,
)


def readSceneData(
    scene: OOTScene,
    scene_properties: OOTSceneProperties,
    sceneHeader: OOTSceneHeaderProperty,
    alternateSceneHeaders: OOTAlternateSceneHeaderProperty,
):
    scene.write_dummy_room_list = scene_properties.write_dummy_room_list
    scene.sceneTableEntry.drawConfig = sceneHeader.sceneTableEntry.drawConfig
    scene.globalObject = getCustomProperty(sceneHeader, "globalObject")
    scene.naviCup = getCustomProperty(sceneHeader, "naviCup")
    scene.skyboxID = getCustomProperty(sceneHeader, "skyboxID")
    scene.skyboxCloudiness = getCustomProperty(sceneHeader, "skyboxCloudiness")
    scene.skyboxLighting = getCustomProperty(sceneHeader, "skyboxLighting")
    scene.lightMode = sceneHeader.skyboxLighting
    scene.mapLocation = getCustomProperty(sceneHeader, "mapLocation")
    scene.cameraMode = getCustomProperty(sceneHeader, "cameraMode")
    scene.musicSeq = getCustomProperty(sceneHeader, "musicSeq")
    scene.nightSeq = getCustomProperty(sceneHeader, "nightSeq")
    scene.audioSessionPreset = getCustomProperty(sceneHeader, "audioSessionPreset")

    if sceneHeader.skyboxLighting == "0x00":  # Time of Day
        scene.lights.append(OOTLight(sceneHeader.timeOfDayLights.dawn))
        scene.lights.append(OOTLight(sceneHeader.timeOfDayLights.day))
        scene.lights.append(OOTLight(sceneHeader.timeOfDayLights.dusk))
        scene.lights.append(OOTLight(sceneHeader.timeOfDayLights.night))
    else:
        for lightProp in sceneHeader.lightList:
            scene.lights.append(OOTLight(lightProp))

    for exitProp in sceneHeader.exitList:
        scene.exitList.append(OOTExit(exitProp))

    scene.writeCutscene = getCustomProperty(sceneHeader, "writeCutscene")
    if scene.writeCutscene:
        scene.csWriteType = getattr(sceneHeader, "csWriteType")
        if scene.csWriteType == "Embedded":
            scene.csEndFrame = getCustomProperty(sceneHeader, "csEndFrame")
            scene.csWriteTerminator = getCustomProperty(sceneHeader, "csWriteTerminator")
            scene.csTermIdx = getCustomProperty(sceneHeader, "csTermIdx")
            scene.csTermStart = getCustomProperty(sceneHeader, "csTermStart")
            scene.csTermEnd = getCustomProperty(sceneHeader, "csTermEnd")
            readCutsceneData(scene, sceneHeader)
        elif scene.csWriteType == "Custom":
            scene.csWriteCustom = getCustomProperty(sceneHeader, "csWriteCustom")
        elif scene.csWriteType == "Object":
            if sceneHeader.csWriteObject is None:
                raise PluginError("No object selected for cutscene reference")
            elif sceneHeader.csWriteObject.ootEmptyType != "Cutscene":
                raise PluginError("Object selected as cutscene is wrong type, must be empty with Cutscene type")
            elif sceneHeader.csWriteObject.parent is not None:
                raise PluginError("Cutscene empty object should not be parented to anything")
            else:
                scene.csWriteObject = convertCutsceneObject(sceneHeader.csWriteObject)

    if alternateSceneHeaders is not None:
        for ec in sceneHeader.extraCutscenes:
            scene.extraCutscenes.append(convertCutsceneObject(ec.csObject))

        scene.collision.cameraData = OOTCameraData(scene.name)

        if not alternateSceneHeaders.childNightHeader.usePreviousHeader:
            scene.childNightHeader = scene.getAlternateHeaderScene(scene.name)
            readSceneData(scene.childNightHeader, scene_properties, alternateSceneHeaders.childNightHeader, None)

        if not alternateSceneHeaders.adultDayHeader.usePreviousHeader:
            scene.adultDayHeader = scene.getAlternateHeaderScene(scene.name)
            readSceneData(scene.adultDayHeader, scene_properties, alternateSceneHeaders.adultDayHeader, None)

        if not alternateSceneHeaders.adultNightHeader.usePreviousHeader:
            scene.adultNightHeader = scene.getAlternateHeaderScene(scene.name)
            readSceneData(scene.adultNightHeader, scene_properties, alternateSceneHeaders.adultNightHeader, None)

        for i in range(len(alternateSceneHeaders.cutsceneHeaders)):
            cutsceneHeaderProp = alternateSceneHeaders.cutsceneHeaders[i]
            cutsceneHeader = scene.getAlternateHeaderScene(scene.name)
            readSceneData(cutsceneHeader, scene_properties, cutsceneHeaderProp, None)
            scene.cutsceneHeaders.append(cutsceneHeader)
    else:
        if len(sceneHeader.extraCutscenes) > 0:
            raise PluginError(
                "Extra cutscenes (not in any header) only belong in the main scene, not alternate headers"
            )


def ootConvertScene(
    originalSceneObj: Object,
    transformMatrix,
    f3dType: str,
    isHWv1: bool,
    sceneName: str,
    DLFormat: DLFormat,
    convertTextureData: bool,
):

    if originalSceneObj.data is not None or originalSceneObj.ootEmptyType != "Scene":
        raise PluginError(originalSceneObj.name + ' is not an empty with the "Scene" empty type.')

    if bpy.context.scene.exportHiddenGeometry:
        hiddenObjs = unhideAllAndGetHiddenList(bpy.context.scene)

    # Don't remove ignore_render, as we want to reuse this for collision
    sceneObj, allObjs = ootDuplicateHierarchy(originalSceneObj, None, True, OOTObjectCategorizer())

    if bpy.context.scene.exportHiddenGeometry:
        hideObjsInList(hiddenObjs)

    roomObjs = [child for child in sceneObj.children if child.data is None and child.ootEmptyType == "Room"]
    if len(roomObjs) == 0:
        raise PluginError("The scene has no child empties with the 'Room' empty type.")

    try:
        scene = OOTScene(sceneName, OOTModel(f3dType, isHWv1, sceneName + "_dl", DLFormat, None))
        readSceneData(scene, sceneObj.fast64.oot.scene, sceneObj.ootSceneHeader, sceneObj.ootAlternateSceneHeaders)
        processedRooms = set()

        for obj in sceneObj.children:
            if obj.data is None and obj.ootEmptyType == "Room":
                processRoom(scene, sceneObj, obj, processedRooms, sceneName, transformMatrix, convertTextureData)
            elif obj.data is None and obj.ootEmptyType == "Water Box":
                ootProcessWaterBox(sceneObj, obj, transformMatrix, scene, 0x3F)
            elif isinstance(obj.data, bpy.types.Camera):
                camPosProp = obj.ootCameraPositionProperty
                readCamPos(camPosProp, obj, scene, sceneObj, transformMatrix)
            elif isinstance(obj.data, bpy.types.Curve) and assertCurveValid(obj):
                readPathProp(obj.ootSplineProperty, obj, scene, sceneObj, sceneName, transformMatrix)

        scene.validateIndices()
        scene.entranceList = sorted(scene.entranceList, key=lambda x: x.startPositionIndex)
        exportCollisionCommon(scene.collision, sceneObj, transformMatrix, True, sceneName)

        ootCleanupScene(originalSceneObj, allObjs)

    except Exception as e:
        ootCleanupScene(originalSceneObj, allObjs)
        raise Exception(str(e))

    return scene
