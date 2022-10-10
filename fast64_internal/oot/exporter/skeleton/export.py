import bpy
from bpy.types import Object
from mathutils import Matrix
from ....f3d.f3d_gbi import DLFormat, FMesh
from ....f3d.f3d_writer import MeshInfo
from ....utility import PluginError, getGroupIndexFromname, cleanupDuplicatedObjects
from ...oot_f3d_writer import ootProcessVertexGroup, getInfoDict
from ...oot_utility import getSortedChildren, checkEmptyName, checkForStartBone, getStartBone
from ...skeleton.utility import ootDuplicateArmature, getGroupIndices
from ..classes.skeleton import OOTSkeleton, OOTLimb
from ...model.classes import OOTModel


def convertArmatureToSkel(
    originalArmatureObj: Object,
    convertTransformMatrix: Matrix,
    fModel: OOTModel,
    name: str,
    convertTextureData: bool,
    skeletonOnly: bool,
    drawLayer: str,
    optimize: bool,
):
    checkEmptyName(name)

    armatureObj, meshObjs = ootDuplicateArmature(originalArmatureObj)

    try:
        skeleton = OOTSkeleton(name)

        if len(armatureObj.children) == 0:
            raise PluginError("No mesh parented to armature.")

        checkForStartBone(armatureObj)
        startBoneName = getStartBone(armatureObj)
        meshObj = meshObjs[0]

        meshInfo = getInfoDict(meshObj)
        getGroupIndices(meshInfo, armatureObj, meshObj, getGroupIndexFromname(meshObj, startBoneName))

        convertTransformMatrix = convertTransformMatrix @ Matrix.Diagonal(armatureObj.scale).to_4x4()

        ootProcessBone(
            fModel,
            startBoneName,
            skeleton,
            0,
            meshObj,
            armatureObj,
            convertTransformMatrix,
            meshInfo,
            convertTextureData,
            name,
            skeletonOnly,
            drawLayer,
            None,
            optimize,
        )

        cleanupDuplicatedObjects(meshObjs + [armatureObj])
        originalArmatureObj.select_set(True)
        bpy.context.view_layer.objects.active = originalArmatureObj

        return skeleton, fModel
    except Exception as e:
        cleanupDuplicatedObjects(meshObjs + [armatureObj])
        originalArmatureObj.select_set(True)
        bpy.context.view_layer.objects.active = originalArmatureObj
        raise Exception(str(e))


def ootProcessBone(
    fModel: OOTModel,
    boneName: str,
    parentLimb,
    nextIndex: int,
    meshObj: Object,
    armatureObj: Object,
    convertTransformMatrix: Matrix,
    meshInfo: MeshInfo,
    convertTextureData: bool,
    namePrefix: str,
    skeletonOnly: bool,
    drawLayer: str,
    lastMaterialName: str,
    optimize: bool,
):
    bone = armatureObj.data.bones[boneName]

    if bone.parent is not None:
        transform = convertTransformMatrix @ bone.parent.matrix_local.inverted() @ bone.matrix_local
    else:
        transform = convertTransformMatrix @ bone.matrix_local

    translate, rotate, scale = transform.decompose()

    groupIndex = getGroupIndexFromname(meshObj, boneName)

    meshInfo.vertexGroupInfo.vertexGroupToLimb[groupIndex] = nextIndex

    if skeletonOnly:
        mesh = None
        hasSkinnedFaces = None
    else:
        mesh, hasSkinnedFaces, lastMaterialName = ootProcessVertexGroup(
            fModel,
            meshObj,
            boneName,
            convertTransformMatrix,
            armatureObj,
            namePrefix,
            meshInfo,
            drawLayer,
            convertTextureData,
            lastMaterialName,
            optimize,
        )

    if bone.ootBoneType == "Custom DL":
        if mesh is not None:
            raise PluginError(
                bone.name
                + " is set to use a custom DL but still has geometry assigned to it. Remove this geometry from this bone."
            )
        else:
            # Dummy data, only used so that name is set correctly
            mesh = FMesh(bone.ootCustomDLName, DLFormat.Static)

    DL = None
    if mesh is not None:
        if not bone.use_deform:
            raise PluginError(
                bone.name
                + " has vertices in its vertex group but is not set to deformable. Make sure to enable deform on this bone."
            )
        DL = mesh.draw

    if isinstance(parentLimb, OOTSkeleton):
        skeleton = parentLimb
        limb = OOTLimb(skeleton.name, boneName, nextIndex, translate, DL, None)
        skeleton.limbRoot = limb
    else:
        limb = OOTLimb(parentLimb.skeletonName, boneName, nextIndex, translate, DL, None)
        parentLimb.children.append(limb)

    limb.isFlex = hasSkinnedFaces
    nextIndex += 1

    # This must be in depth-first order to match the OoT SkelAnime draw code, so
    # the bones are listed in the file in the same order as they are drawn. This
    # is needed to enable the programmer to get the limb indices and to enable
    # optimization between limbs.
    childrenNames = getSortedChildren(armatureObj, bone)
    for childName in childrenNames:
        nextIndex, lastMaterialName = ootProcessBone(
            fModel,
            childName,
            limb,
            nextIndex,
            meshObj,
            armatureObj,
            convertTransformMatrix,
            meshInfo,
            convertTextureData,
            namePrefix,
            skeletonOnly,
            drawLayer,
            lastMaterialName,
            optimize,
        )

    return nextIndex, lastMaterialName
