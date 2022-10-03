import bpy
from math import radians, degrees
from mathutils import Quaternion, Matrix
from bpy.types import Mesh, Object
from ...utility import PluginError, checkIdentityRotation, toAlnum
from ...f3d.f3d_writer import TriangleConverterInfo, getInfoDict, saveStaticModel
from ..oot_collision_classes import OOTWaterBox, OOTCameraPosData, decomp_compat_map_CameraSType
from ..oot_collision import OOTCameraPositionProperty
from ..oot_utility import CullGroup, checkUniformScale, getCustomProperty, ootConvertRotation, ootConvertTranslation
from ..oot_spline import ootConvertPath
from .classes.scene import OOTScene
from .classes.room import OOTDLGroup, OOTRoomMesh


def getConvertedTransform(transformMatrix, sceneObj: Object, obj: Object, handleOrientation: bool):
    # Hacky solution to handle Z-up to Y-up conversion
    # We cannot apply rotation to empty, as that modifies scale
    if handleOrientation:
        orientation = Quaternion((1, 0, 0), radians(90.0))
    else:
        orientation = Matrix.Identity(4)
    return getConvertedTransformWithOrientation(transformMatrix, sceneObj, obj, orientation)


def getConvertedTransformWithOrientation(transformMatrix, sceneObj: Object, obj: Object, orientation):
    relativeTransform = transformMatrix @ sceneObj.matrix_world.inverted() @ obj.matrix_world
    blenderTranslation, blenderRotation, scale = relativeTransform.decompose()
    rotation = blenderRotation @ orientation
    convertedTranslation = ootConvertTranslation(blenderTranslation)
    convertedRotation = ootConvertRotation(rotation)

    return convertedTranslation, convertedRotation, scale, rotation


def ootProcessWaterBox(sceneObj: Object, obj: Object, transformMatrix, scene: OOTScene, roomIndex: int):
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


def ootProcessLOD(
    roomMesh: OOTRoomMesh,
    DLGroup: OOTDLGroup,
    sceneObj: Object,
    obj: Object,
    transformMatrix,
    convertTextureData: bool,
    LODHierarchyObject: Object | None,
):
    relativeTransform = transformMatrix @ sceneObj.matrix_world.inverted() @ obj.matrix_world
    translation, rotation, scale = relativeTransform.decompose()
    ootTranslation = ootConvertTranslation(translation)

    LODHierarchyObject = obj
    name = toAlnum(roomMesh.model.name + "_" + obj.name + "_lod")
    opaqueLOD = roomMesh.model.addLODGroup(name + "_opaque", ootTranslation, obj.f3d_lod_always_render_farthest)
    transparentLOD = roomMesh.model.addLODGroup(
        name + "_transparent", ootTranslation, obj.f3d_lod_always_render_farthest
    )

    index = 0
    for childObj in obj.children:
        # This group will not be converted to C directly, but its display lists will be converted through the FLODGroup.
        childDLGroup = OOTDLGroup(name + str(index), roomMesh.model.DLFormat)
        index += 1

        if childObj.data is None and childObj.ootEmptyType == "LOD":
            ootProcessLOD(
                roomMesh, childDLGroup, sceneObj, childObj, transformMatrix, convertTextureData, LODHierarchyObject
            )
        else:
            ootProcessMesh(
                roomMesh, childDLGroup, sceneObj, childObj, transformMatrix, convertTextureData, LODHierarchyObject
            )

        # We handle case with no geometry, for the cases where we have "gaps" in the LOD hierarchy.
        # This can happen if a LOD does not use transparency while the levels above and below it does.
        childDLGroup.createDLs()
        childDLGroup.terminateDLs()

        # Add lod AFTER processing hierarchy, so that DLs will be built by then
        opaqueLOD.add_lod(childDLGroup.opaque, childObj.f3d_lod_z * bpy.context.scene.ootBlenderScale)
        transparentLOD.add_lod(childDLGroup.transparent, childObj.f3d_lod_z * bpy.context.scene.ootBlenderScale)

    opaqueLOD.create_data()
    transparentLOD.create_data()

    DLGroup.addDLCall(opaqueLOD.draw, "Opaque")
    DLGroup.addDLCall(transparentLOD.draw, "Transparent")


# This function should be called on a copy of an object
# The copy will have modifiers / scale applied and will be made single user
# When we duplicated obj hierarchy we stripped all ignore_renders from hierarchy.
def ootProcessMesh(
    roomMesh: OOTRoomMesh,
    DLGroup: OOTDLGroup,
    sceneObj: Object,
    obj: Object,
    transformMatrix,
    convertTextureData: bool,
    LODHierarchyObject: Object | None,
):
    relativeTransform = transformMatrix @ sceneObj.matrix_world.inverted() @ obj.matrix_world
    translation, rotation, scale = relativeTransform.decompose()

    if obj.data is None and obj.ootEmptyType == "Cull Group":
        if LODHierarchyObject is not None:
            raise PluginError(
                obj.name
                + " cannot be used as a cull group because it is "
                + "in the sub-hierarchy of the LOD group empty "
                + LODHierarchyObject.name
            )

        checkUniformScale(scale, obj)
        DLGroup = roomMesh.addMeshGroup(
            CullGroup(ootConvertTranslation(translation), scale, obj.empty_display_size)
        ).DLGroup

    elif isinstance(obj.data, Mesh) and not obj.ignore_render:
        triConverterInfo = TriangleConverterInfo(obj, None, roomMesh.model.f3d, relativeTransform, getInfoDict(obj))
        fMeshes = saveStaticModel(
            triConverterInfo,
            roomMesh.model,
            obj,
            relativeTransform,
            roomMesh.model.name,
            convertTextureData,
            False,
            "oot",
        )
        if fMeshes is not None:
            for drawLayer, fMesh in fMeshes.items():
                DLGroup.addDLCall(fMesh.draw, drawLayer)

    alphabeticalChildren = sorted(obj.children, key=lambda childObj: childObj.original_name.lower())
    for childObj in alphabeticalChildren:
        if childObj.data is None and childObj.ootEmptyType == "LOD":
            ootProcessLOD(
                roomMesh, DLGroup, sceneObj, childObj, transformMatrix, convertTextureData, LODHierarchyObject
            )
        else:
            ootProcessMesh(
                roomMesh, DLGroup, sceneObj, childObj, transformMatrix, convertTextureData, LODHierarchyObject
            )


def readCamPos(camPosProp: OOTCameraPositionProperty, obj: Object, scene: OOTScene, sceneObj: Object, transformMatrix):
    # Camera faces opposite direction
    orientation = Quaternion((0, 1, 0), radians(180.0))
    translation, rotation, scale, orientedRotation = getConvertedTransformWithOrientation(
        transformMatrix, sceneObj, obj, orientation
    )
    camPosProp = obj.ootCameraPositionProperty
    index = camPosProp.index
    # TODO: FOV conversion?
    if index in scene.collision.cameraData.camPosDict:
        raise PluginError("Error: Repeated camera position index: " + str(index))
    if camPosProp.camSType == "Custom":
        camSType = camPosProp.camSTypeCustom
    else:
        camSType = decomp_compat_map_CameraSType.get(camPosProp.camSType, camPosProp.camSType)
    scene.collision.cameraData.camPosDict[index] = OOTCameraPosData(
        camSType,
        camPosProp.hasPositionData,
        translation,
        rotation,
        int(round(degrees(obj.data.angle))),
        camPosProp.jfifID,
    )


def readPathProp(pathProp, obj: Object, scene: OOTScene, sceneObj: Object, sceneName: str, transformMatrix):
    relativeTransform = transformMatrix @ sceneObj.matrix_world.inverted() @ obj.matrix_world
    index = obj.ootSplineProperty.index
    if index in scene.pathList:
        raise PluginError("Error: " + obj.name + "has a repeated spline index: " + str(index))
    scene.pathList[index] = ootConvertPath(sceneName, index, obj, relativeTransform)