import bpy
import os
import re
import math

from bpy.types import Object

from ..utility import (
    PluginError,
    prop_split,
    getDataFromFile,
    saveDataToFile,
    attemptModifierApply,
    setOrigin,
    applyRotation,
    cleanupDuplicatedObjects,
    ootGetSceneOrRoomHeader,
    hexOrDecInt,
    binOps,
)


class OOTObjectCategorizer:
    def __init__(self):
        self.sceneObj = None
        self.roomObjs = []
        self.actors = []
        self.transitionActors = []
        self.meshes = []
        self.entrances = []
        self.waterBoxes = []

    def sortObjects(self, allObjs):
        for obj in allObjs:
            if obj.type == "EMPTY":
                if obj.ootEmptyType == "Actor":
                    self.actors.append(obj)
                elif obj.ootEmptyType == "Transition Actor":
                    self.transitionActors.append(obj)
                elif obj.ootEmptyType == "Entrance":
                    self.entrances.append(obj)
                elif obj.ootEmptyType == "Water Box":
                    self.waterBoxes.append(obj)
                elif obj.ootEmptyType == "Room":
                    self.roomObjs.append(obj)
                elif obj.ootEmptyType == "Scene":
                    self.sceneObj = obj
            elif obj.type == "MESH":
                self.meshes.append(obj)


def test_game_type(game: str):
    return bpy.context.scene.gameEditorMode == game


def get_path(exportPath, isCustomExport, subPath, folderName, makeIfNotExists, useFolderForCustom):
    if isCustomExport:
        path = bpy.path.abspath(os.path.join(exportPath, (folderName if useFolderForCustom else "")))
    else:
        if bpy.context.scene.z64_decomp_path == "":
            raise PluginError("Decomp base path is empty.")
        path = bpy.path.abspath(os.path.join(os.path.join(bpy.context.scene.z64_decomp_path, subPath), folderName))

    if not os.path.exists(path):
        if isCustomExport or makeIfNotExists:
            os.makedirs(path)
        else:
            raise PluginError(path + " does not exist.")

    return path


def get_object_path(isCustomExport: bool, exportPath: str, folderName: str, include_extracted: bool) -> str:
    extracted = bpy.context.scene.fast64.z64.get_extracted_path() if include_extracted else "."

    if isCustomExport:
        filepath = exportPath
    else:
        filepath = os.path.join(
            get_path(
                exportPath,
                isCustomExport,
                f"{extracted}/assets/objects/",
                folderName,
                False,
                False,
            ),
            folderName + ".c",
        )
    return filepath


def get_z64_scale(actorScale: float) -> float:
    return bpy.context.scene.z64_blender_scale * actorScale


def replace_match_content(data: str, newContent: str, match: re.Match, index: int) -> str:
    return data[: match.start(index)] + newContent + data[match.end(index) :]


def addIncludeFilesExtension(objectName, objectPath, assetName, extension):
    include = '#include "' + assetName + "." + extension + '"\n'
    if not os.path.exists(objectPath):
        raise PluginError(objectPath + " does not exist.")
    path = os.path.join(objectPath, objectName + "." + extension)
    if not os.path.exists(path):
        # workaround for exporting to an object that doesn't exist in assets/
        data = ""
    else:
        data = getDataFromFile(path)

    if include not in data:
        data += "\n" + include

    # Save this regardless of modification so it will be recompiled.
    saveDataToFile(path, data)


def addIncludeFiles(objectName, objectPath, assetName):
    addIncludeFilesExtension(objectName, objectPath, assetName, "h")
    addIncludeFilesExtension(objectName, objectPath, assetName, "c")


def ootCleanupScene(originalSceneObj, allObjs):
    cleanupDuplicatedObjects(allObjs)
    originalSceneObj.select_set(True)
    bpy.context.view_layer.objects.active = originalSceneObj


def ootSelectMeshChildrenOnly(obj, includeEmpties):
    isMesh = obj.type == "MESH"
    isEmpty = (obj.type == "EMPTY" or obj.type == "CAMERA" or obj.type == "CURVE") and includeEmpties
    if isMesh or isEmpty:
        obj.select_set(True)
        obj.original_name = obj.name
    for child in obj.children:
        ootSelectMeshChildrenOnly(child, includeEmpties)


# This also sets all origins relative to the scene object.
def ootDuplicateHierarchy(obj, ignoreAttr, includeEmpties, objectCategorizer) -> tuple[Object, list[Object]]:
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
            applyRotation([tempObj], math.radians(90), "X")
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
