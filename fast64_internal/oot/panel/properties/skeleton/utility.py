import bpy
from re import search, escape, DOTALL
from bpy.types import Object
from bpy.ops import pose, object
from .....f3d.f3d_writer import MeshInfo
from .....utility import PluginError, attemptModifierApply, cleanupDuplicatedObjects, getGroupNameFromIndex, setOrigin
from .classes import OOTVertexGroupInfo


def getGroupIndexOfVert(vertex, armatureObj: Object, obj: Object, rootGroupIndex: int):
    # is ``vertex`` type ``MeshVertex``?
    actualGroups = []
    nonBoneGroups = []

    for group in vertex.groups:
        groupName = getGroupNameFromIndex(obj, group.group)

        if groupName is not None:
            if groupName in armatureObj.data.bones:
                actualGroups.append(group)
            else:
                nonBoneGroups.append(groupName)

    if len(actualGroups) == 0:
        return rootGroupIndex

    vertGroup = actualGroups[0]

    for group in actualGroups:
        if group.weight > vertGroup.weight:
            vertGroup = group

    return vertGroup.group


def getGroupIndices(meshInfo: MeshInfo, armatureObj: Object, meshObj: Object, rootGroupIndex: int):
    meshInfo.vertexGroupInfo = OOTVertexGroupInfo()

    for vertex in meshObj.data.vertices:
        meshInfo.vertexGroupInfo.vertexGroups[vertex.index] = getGroupIndexOfVert(
            vertex, armatureObj, meshObj, rootGroupIndex
        )


def ootDuplicateArmature(originalArmatureObj: Object):
    # Duplicate objects to apply scale / modifiers / linked data
    object.select_all(action="DESELECT")

    for originalMeshObj in [obj for obj in originalArmatureObj.children if isinstance(obj.data, bpy.types.Mesh)]:
        originalMeshObj.select_set(True)
        originalMeshObj.original_name = originalMeshObj.name

    originalArmatureObj.select_set(True)
    originalArmatureObj.original_name = originalArmatureObj.name
    bpy.context.view_layer.objects.active = originalArmatureObj
    object.duplicate()

    armatureObj = bpy.context.view_layer.objects.active
    meshObjs = [obj for obj in bpy.context.selected_objects if obj is not armatureObj]

    try:
        for obj in meshObjs:
            setOrigin(armatureObj, obj)

        object.select_all(action="DESELECT")
        armatureObj.select_set(True)
        bpy.context.view_layer.objects.active = armatureObj
        object.transform_apply(location=False, rotation=False, scale=True, properties=False)

        # Apply modifiers/data to mesh objs
        object.select_all(action="DESELECT")

        for obj in meshObjs:
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj

        object.make_single_user(obdata=True)
        object.transform_apply(location=False, rotation=True, scale=True, properties=False)

        for selectedObj in meshObjs:
            object.select_all(action="DESELECT")
            selectedObj.select_set(True)
            bpy.context.view_layer.objects.active = selectedObj

            for modifier in selectedObj.modifiers:
                attemptModifierApply(modifier)

        # Apply new armature rest pose
        object.select_all(action="DESELECT")
        bpy.context.view_layer.objects.active = armatureObj
        object.mode_set(mode="POSE")
        pose.armature_apply()
        object.mode_set(mode="OBJECT")

        return armatureObj, meshObjs
    except Exception as e:
        cleanupDuplicatedObjects(meshObjs + [armatureObj])
        originalArmatureObj.select_set(True)
        bpy.context.view_layer.objects.active = originalArmatureObj
        raise Exception(str(e))


# those functions are used for both import and export


def ootGetLimbs(skeletonData: str, limbsName: str, continueOnError: bool):
    matchResult = search(
        "(static\s*)?void\s*\*\s*" + escape(limbsName) + "\s*\[\s*[0-9]*\s*\]\s*=\s*\{([^\}]*)\}\s*;\s*",
        skeletonData,
        DOTALL,
    )

    if matchResult is None:
        if continueOnError:
            return None
        else:
            raise PluginError("Cannot find skeleton limbs named " + limbsName)

    return matchResult


def ootGetLimb(skeletonData: str, limbName: str, continueOnError: bool):
    matchResult = search("([A-Za-z0-9\_]*)Limb\s*" + escape(limbName), skeletonData)

    if matchResult is None:
        if continueOnError:
            return None
        else:
            raise PluginError("Cannot find skeleton limb named " + limbName)

    limbType = matchResult.group(1)

    if limbType == "Lod":
        dlRegex = "\{\s*([^,\s]*)\s*,\s*([^,\s]*)\s*\}"
    else:
        dlRegex = "([^,\s]*)"

    matchResult = search(
        "[A-Za-z0-9\_]*Limb\s*"
        + escape(limbName)
        + "\s*=\s*\{\s*\{\s*([^,\s]*)\s*,\s*([^,\s]*)\s*,\s*([^,\s]*)\s*\},\s*([^, ]*)\s*,\s*([^, ]*)\s*,\s*"
        + dlRegex
        + "\s*\}\s*;\s*",
        skeletonData,
        DOTALL,
    )

    if matchResult is None:
        if continueOnError:
            return None
        else:
            raise PluginError("Cannot handle skeleton limb named " + limbName + " of type " + limbType)

    return matchResult


def ootGetSkeleton(skeletonData: str, skeletonName: str, continueOnError: bool):
    # TODO: Does this handle non flex skeleton?
    matchResult = search(
        "(Flex)?SkeletonHeader\s*"
        + escape(skeletonName)
        + "\s*=\s*\{\s*\{?\s*([^,\s]*)\s*,\s*([^,\s\}]*)\s*\}?\s*(,\s*([^,\s]*))?\s*\}\s*;\s*",
        skeletonData,
    )

    if matchResult is None:
        if continueOnError:
            return None
        else:
            raise PluginError("Cannot find skeleton named " + skeletonName)

    return matchResult
