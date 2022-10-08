import bpy
from math import radians
from mathutils import Matrix, Vector
from ....utility import hexOrDecInt, applyRotation
from ....f3d.f3d_gbi import F3D
from ....f3d.f3d_parser import getImportData, parseF3D
from ...model import OOTF3DContext
from ...panel.viewport.skeleton.classes import OOTSkeletonImportSettings
from ...skeleton.utility import ootGetLimb, ootGetLimbs, ootGetSkeleton
from ..classes.skeleton import OOTDLEntry


def ootImportSkeletonC(
    filepaths: list[str], actorScale: float, basePath: str, importSettings: OOTSkeletonImportSettings
):
    skeletonName = importSettings.name
    removeDoubles = importSettings.removeDoubles
    importNormals = importSettings.importNormals
    drawLayer = importSettings.drawLayer

    skeletonData = getImportData(filepaths)

    matchResult = ootGetSkeleton(skeletonData, skeletonName, False)
    limbsName = matchResult.group(2)

    matchResult = ootGetLimbs(skeletonData, limbsName, False)
    limbsData = matchResult.group(2)
    limbList = [entry.strip()[1:] for entry in limbsData.split(",")]

    isLOD, armatureObj = ootBuildSkeleton(
        skeletonName, skeletonData, limbList, actorScale, removeDoubles, importNormals, False, basePath, drawLayer
    )

    if isLOD:
        isLOD, LODArmatureObj = ootBuildSkeleton(
            skeletonName, skeletonData, limbList, actorScale, removeDoubles, importNormals, True, basePath, drawLayer
        )
        armatureObj.ootFarLOD = LODArmatureObj


def ootBuildSkeleton(
    skeletonName: str,
    skeletonData: str,
    limbList: list[str],
    actorScale: float,
    removeDoubles: bool,
    importNormals: bool,
    useFarLOD: bool,
    basePath: str,
    drawLayer: str,
):
    lodString = "_lod" if useFarLOD else ""

    # Create new skinned mesh
    meshName = f"{skeletonName}_mesh{lodString}"
    mesh = bpy.data.meshes.new(meshName)
    obj = bpy.data.objects.new(meshName, mesh)
    bpy.context.scene.collection.objects.link(obj)

    # Create new armature
    armature = bpy.data.armatures.new(skeletonName + lodString)
    armatureObj = bpy.data.objects.new(skeletonName + lodString, armature)
    armatureObj.show_in_front = True
    armatureObj.ootDrawLayer = drawLayer

    bpy.context.scene.collection.objects.link(armatureObj)
    bpy.context.view_layer.objects.active = armatureObj

    f3dContext = OOTF3DContext(F3D("F3DEX2/LX2", False), limbList, basePath)
    f3dContext.mat().draw_layer.oot = armatureObj.ootDrawLayer
    transformMatrix = Matrix.Scale(1 / actorScale, 4)
    isLOD = ootAddLimbRecursively(0, skeletonData, obj, armatureObj, transformMatrix, None, f3dContext, useFarLOD)

    for dlEntry in f3dContext.dlList:
        limbName = f3dContext.getLimbName(dlEntry.limbIndex)
        boneName = f3dContext.getBoneName(dlEntry.limbIndex)
        parseF3D(
            skeletonData,
            dlEntry.dlName,
            obj,
            f3dContext.matrixData[limbName],
            limbName,
            boneName,
            "oot",
            drawLayer,
            f3dContext,
        )

        if f3dContext.isBillboard:
            armatureObj.data.bones[boneName].ootDynamicTransform.billboard = True

        f3dContext.clearMaterial()  # THIS IS IMPORTANT

    f3dContext.createMesh(obj, removeDoubles, importNormals)
    armatureObj.location = bpy.context.scene.cursor.location

    # Set bone rotation mode.
    bpy.ops.object.select_all(action="DESELECT")
    armatureObj.select_set(True)
    bpy.context.view_layer.objects.active = armatureObj
    bpy.ops.object.mode_set(mode="POSE")

    for bone in armatureObj.pose.bones:
        bone.rotation_mode = "XYZ"

    # Apply mesh to armature.
    if bpy.context.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")

    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    armatureObj.select_set(True)
    bpy.context.view_layer.objects.active = armatureObj
    bpy.ops.object.parent_set(type="ARMATURE")

    applyRotation([armatureObj], radians(-90), "X")

    return isLOD, armatureObj


def ootAddBone(armatureObj, boneName, parentBoneName, currentTransform, loadDL):
    if bpy.context.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = armatureObj
    bpy.ops.object.mode_set(mode="EDIT")
    bone = armatureObj.data.edit_bones.new(boneName)
    bone.use_connect = False
    if parentBoneName is not None:
        bone.parent = armatureObj.data.edit_bones[parentBoneName]
    bone.head = currentTransform @ Vector((0, 0, 0))
    bone.tail = bone.head + (currentTransform.to_quaternion() @ Vector((0, 0.3, 0)))

    # Connect bone to parent if it is possible without changing parent direction.

    if parentBoneName is not None:
        nodeOffsetVector = Vector(bone.head - bone.parent.head)
        # set fallback to nonzero to avoid creating zero length bones
        if nodeOffsetVector.angle(bone.parent.tail - bone.parent.head, 1) < 0.0001 and loadDL:
            for child in bone.parent.children:
                if child != bone:
                    child.use_connect = False
            bone.parent.tail = bone.head
            bone.use_connect = True
        elif bone.head == bone.parent.head and bone.tail == bone.parent.tail:
            bone.tail += currentTransform.to_quaternion() @ Vector((0, 0.2, 0))

    if bpy.context.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")


def ootAddLimbRecursively(
    limbIndex, skeletonData, obj, armatureObj, parentTransform, parentBoneName, f3dContext, useFarLOD
):

    limbName = f3dContext.getLimbName(limbIndex)
    boneName = f3dContext.getBoneName(limbIndex)
    matchResult = ootGetLimb(skeletonData, limbName, False)

    isLOD = matchResult.lastindex > 6

    if isLOD and useFarLOD:
        dlName = matchResult.group(7)
    else:
        dlName = matchResult.group(6)

    # Animations override the root translation, so we just ignore importing them as well.
    if limbIndex == 0:
        translation = [0, 0, 0]
    else:
        translation = [
            hexOrDecInt(matchResult.group(1)),
            hexOrDecInt(matchResult.group(2)),
            hexOrDecInt(matchResult.group(3)),
        ]

    LIMB_DONE = 0xFF
    nextChildIndexStr = matchResult.group(4)
    nextChildIndex = LIMB_DONE if nextChildIndexStr == "LIMB_DONE" else hexOrDecInt(nextChildIndexStr)
    nextSiblingIndexStr = matchResult.group(5)
    nextSiblingIndex = LIMB_DONE if nextSiblingIndexStr == "LIMB_DONE" else hexOrDecInt(nextSiblingIndexStr)

    currentTransform = parentTransform @ Matrix.Translation(Vector(translation))
    f3dContext.matrixData[limbName] = currentTransform
    loadDL = dlName != "NULL"

    ootAddBone(armatureObj, boneName, parentBoneName, currentTransform, loadDL)

    # DLs can access bone transforms not yet processed.
    # Therefore were delay F3D parsing until after skeleton is processed.
    if loadDL:
        f3dContext.dlList.append(OOTDLEntry(dlName, limbIndex))

    if nextChildIndex != LIMB_DONE:
        isLOD |= ootAddLimbRecursively(
            nextChildIndex, skeletonData, obj, armatureObj, currentTransform, boneName, f3dContext, useFarLOD
        )

    if nextSiblingIndex != LIMB_DONE:
        isLOD |= ootAddLimbRecursively(
            nextSiblingIndex, skeletonData, obj, armatureObj, parentTransform, parentBoneName, f3dContext, useFarLOD
        )

    return isLOD
