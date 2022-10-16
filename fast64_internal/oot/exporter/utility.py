import bpy
from os import path as p, makedirs
from math import degrees, radians
from mathutils import Matrix
from bpy.types import Mesh, Object
from ...f3d.f3d_writer import TriangleConverterInfo, getInfoDict, saveStaticModel
from .classes.export import CullGroup, OOTObjectCategorizer
from .classes.room import OOTDLGroup, OOTRoomMesh

from ...utility import (
    PluginError,
    toAlnum,
    getDataFromFile,
    saveDataToFile,
    setOrigin,
    attemptModifierApply,
    applyRotation,
    cleanupDuplicatedObjects,
)


def checkUniformScale(scale: list[int], obj: Object):
    if abs(scale[0] - scale[1]) > 0.01 or abs(scale[1] - scale[2]) > 0.01 or abs(scale[0] - scale[2]) > 0.01:
        raise PluginError("Cull group " + obj.name + " must have a uniform scale.")


def getCustomProperty(data, prop: str):
    value = getattr(data, prop)
    return value if value != "Custom" else getattr(data, prop + str("Custom"))


def convertIntTo2sComplement(value: int, length: int, signed: bool):
    # is it really required to use ``round`` there?
    return int.from_bytes(round(value).to_bytes(length, "big", signed=signed), "big")


def ootConvertTranslation(translation: list[int]):
    return [int(round(value)) for value in translation]


def ootConvertRotation(rotation):
    # see BINANG_TO_DEGF
    return [round((degrees(value) % 360) / 360 * (2**16)) % (2**16) for value in rotation.to_euler()]


def getConvertedTransformWithOrientation(transformMatrix: Matrix, sceneObj: Object, obj: Object, orientation: Matrix):
    relativeTransform: Matrix = transformMatrix @ sceneObj.matrix_world.inverted() @ obj.matrix_world
    blenderTranslation, blenderRotation, scale = relativeTransform.decompose()
    rotation = blenderRotation @ orientation
    convertedTranslation = ootConvertTranslation(blenderTranslation)
    convertedRotation = ootConvertRotation(rotation)

    return convertedTranslation, convertedRotation, scale, rotation


def ootProcessLOD(
    roomMesh: OOTRoomMesh,
    DLGroup: OOTDLGroup,
    sceneObj: Object,
    obj: Object,
    transformMatrix: Matrix,
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
    transformMatrix: Matrix,
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
        DLGroup = roomMesh.newMeshGroup(
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


def addIncludeFilesExtension(objectName: str, objectPath: str, assetName: str, extension: str):
    include = '#include "' + assetName + "." + extension + '"\n'
    if not p.exists(objectPath):
        raise PluginError(objectPath + " does not exist.")
    path = p.join(objectPath, objectName + "." + extension)
    data = getDataFromFile(path)

    if include not in data:
        data += "\n" + include

    # Save this regardless of modification so it will be recompiled.
    saveDataToFile(path, data)


def addIncludeFiles(objectName: str, objectPath: str, assetName: str):
    addIncludeFilesExtension(objectName, objectPath, assetName, "h")
    addIncludeFilesExtension(objectName, objectPath, assetName, "c")


# This also sets all origins relative to the scene object.
def ootDuplicateHierarchy(obj: Object, ignoreAttr: bool, includeEmpties: bool, objectCategorizer: OOTObjectCategorizer):
    # Duplicate objects to apply scale / modifiers / linked data
    bpy.ops.object.select_all(action="DESELECT")
    ootSelectMeshChildrenOnly(obj, includeEmpties)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.duplicate()
    try:
        tempObj = bpy.context.view_layer.objects.active
        allObjs = bpy.context.selected_objects
        bpy.ops.object.make_single_user(obdata=True)

        objectCategorizer.sortObjects(allObjs)
        meshObjs = objectCategorizer.meshes
        bpy.ops.object.select_all(action="DESELECT")
        for selectedObj in meshObjs:
            selectedObj.select_set(True)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True, properties=False)

        for selectedObj in meshObjs:
            bpy.ops.object.select_all(action="DESELECT")
            selectedObj.select_set(True)
            bpy.context.view_layer.objects.active = selectedObj
            for modifier in selectedObj.modifiers:
                attemptModifierApply(modifier)
        for selectedObj in meshObjs:
            setOrigin(obj, selectedObj)
        if ignoreAttr is not None:
            for selectedObj in meshObjs:
                if getattr(selectedObj, ignoreAttr):
                    for child in selectedObj.children:
                        bpy.ops.object.select_all(action="DESELECT")
                        child.select_set(True)
                        bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
                        selectedObj.parent.select_set(True)
                        bpy.ops.object.parent_set(keep_transform=True)
                    selectedObj.parent = None

        # Assume objects with these types of constraints are parented, and are
        # intended to be parented in-game, i.e. rendered as an extra DL alongside
        # a skeletal mesh, e.g. for a character to be wearing or holding it.
        # In this case we purely want the transformation of the object relative
        # to whatever it's parented to. Getting rid of the constraint and then
        # doing transform_apply() sets up this transformation.
        hasConstraint = False
        for constraint in tempObj.constraints:
            if (
                constraint.type
                in {
                    "COPY_LOCATION",
                    "COPY_ROTATION",
                    "COPY_SCALE",
                    "COPY_TRANSFORMS",
                    "TRANSFORM",
                    "CHILD_OF",
                    "CLAMP_TO",
                    "DAMPED_TRACK",
                    "LOCKED_TRACK",
                    "TRACK_TO",
                }
                and not constraint.mute
            ):
                hasConstraint = True
                tempObj.constraints.remove(constraint)
        if not hasConstraint:
            # For normal objects, the game's coordinate system is 90 degrees
            # away from Blender's.
            applyRotation([tempObj], radians(90), "X")
        else:
            # This is a relative transform we care about so the 90 degrees
            # doesn't matter (since they're both right-handed).
            print("Applying transform")
            bpy.ops.object.select_all(action="DESELECT")
            tempObj.select_set(True)
            bpy.context.view_layer.objects.active = tempObj
            bpy.ops.object.transform_apply()

        return tempObj, allObjs
    except Exception as e:
        cleanupDuplicatedObjects(allObjs)
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        raise Exception(str(e))


def ootSelectMeshChildrenOnly(obj: Object, includeEmpties: bool):
    isMesh = isinstance(obj.data, bpy.types.Mesh)
    isEmpty = (
        obj.data is None or isinstance(obj.data, bpy.types.Camera) or isinstance(obj.data, bpy.types.Curve)
    ) and includeEmpties
    if isMesh or isEmpty:
        obj.select_set(True)
        obj.original_name = obj.name
    for child in obj.children:
        ootSelectMeshChildrenOnly(child, includeEmpties)


def ootCleanupScene(originalSceneObj: Object, allObjs: list[Object]):
    cleanupDuplicatedObjects(allObjs)
    originalSceneObj.select_set(True)
    bpy.context.view_layer.objects.active = originalSceneObj


def checkEmptyName(name: str):
    if name == "":
        raise PluginError("No name entered for the exporter.")


def ootGetPath(
    exportPath: str,
    isCustomExport: bool,
    subPath: str,
    folderName: str,
    makeIfNotExists: bool,
    useFolderForCustom: bool,
):
    if isCustomExport:
        path = bpy.path.abspath(p.join(exportPath, (folderName if useFolderForCustom else "")))
    else:
        if bpy.context.scene.ootDecompPath == "":
            raise PluginError("Decomp base path is empty.")
        path = bpy.path.abspath(p.join(bpy.context.scene.ootDecompPath, subPath + folderName))

    if not p.exists(path):
        if isCustomExport or makeIfNotExists:
            makedirs(path)
        else:
            raise PluginError(path + " does not exist.")

    return path
