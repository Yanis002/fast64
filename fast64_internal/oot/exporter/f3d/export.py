from mathutils import Matrix
from bpy.types import Object
from ....utility import getGroupIndexFromname
from ...model.classes import OOTModel
from ...exporter.classes.f3d import OOTTriangleConverterInfo

from ....f3d.f3d_writer import (
    MeshInfo,
    checkForF3dMaterialInFaces,
    saveOrGetF3DMaterial,
    saveMeshWithLargeTexturesByFaces,
    saveMeshByFaces,
)


# returns:
# 	mesh,
# 	anySkinnedFaces (to determine if skeleton should be flex)
def ootProcessVertexGroup(
    fModel: OOTModel,
    meshObj: Object,
    vertexGroup: str,
    convertTransformMatrix: Matrix,
    armatureObj: Object,
    namePrefix: str,
    meshInfo: MeshInfo,
    drawLayerOverride: str,
    convertTextureData: bool,
    lastMaterialName: str,
    optimize: bool,
):
    if not optimize:
        lastMaterialName = None

    currentGroupIndex = getGroupIndexFromname(meshObj, vertexGroup)
    nextDLIndex = len(meshInfo.vertexGroupInfo.vertexGroupToMatrixIndex)

    vertIndices = [
        vert.index
        for vert in meshObj.data.vertices
        if meshInfo.vertexGroupInfo.vertexGroups[vert.index] == currentGroupIndex
    ]

    if len(vertIndices) == 0:
        print(f"No vert indices in {vertexGroup}")
        return None, False, lastMaterialName

    bone = armatureObj.data.bones[vertexGroup]

    # dict of material_index keys to face array values
    groupFaces = {}

    hasSkinnedFaces = False
    handledFaces = []
    anyConnectedToUnhandledBone = False

    for vertIndex in vertIndices:
        if vertIndex in meshInfo.vert:
            for face in meshInfo.vert[vertIndex]:
                # Ignore repeat faces
                if face not in handledFaces:
                    connectedToUnhandledBone = False

                    # A Blender loop is interpreted as face + loop index
                    for i in range(3):
                        faceVertIndex = face.vertices[i]
                        vertGroupIndex = meshInfo.vertexGroupInfo.vertexGroups[faceVertIndex]

                        if vertGroupIndex != currentGroupIndex:
                            hasSkinnedFaces = True

                        if vertGroupIndex not in meshInfo.vertexGroupInfo.vertexGroupToLimb:
                            # Connected to a bone not processed yet
                            # These skinned faces will be handled by that limb
                            connectedToUnhandledBone = True
                            anyConnectedToUnhandledBone = True
                            break

                    if not connectedToUnhandledBone:
                        if face.material_index not in groupFaces:
                            groupFaces[face.material_index] = []
                        groupFaces[face.material_index].append(face)

                        handledFaces.append(face)

    if len(groupFaces) == 0:
        print(f"No faces in {vertexGroup}")

        # OOT will only allocate matrix if DL exists.
        # This doesn't handle case where vertices belong to a limb, but not triangles.
        # Therefore we create a dummy DL
        if anyConnectedToUnhandledBone:
            fMesh = fModel.addMesh(vertexGroup, namePrefix, drawLayerOverride, False, bone)
            fModel.endDraw(fMesh, bone)
            meshInfo.vertexGroupInfo.vertexGroupToMatrixIndex[currentGroupIndex] = nextDLIndex
            return fMesh, False, lastMaterialName
        else:
            return None, False, lastMaterialName

    meshInfo.vertexGroupInfo.vertexGroupToMatrixIndex[currentGroupIndex] = nextDLIndex
    triConverterInfo = OOTTriangleConverterInfo(meshObj, armatureObj.data, fModel.f3d, convertTransformMatrix, meshInfo)

    if optimize:
        # If one of the materials we need to draw is the currently loaded material,
        # do this one first.
        newGroupFaces = {
            material_index: faces
            for material_index, faces in groupFaces.items()
            if meshObj.material_slots[material_index].material.name == lastMaterialName
        }

        newGroupFaces.update(groupFaces)
        groupFaces = newGroupFaces

    # Usually we would separate DLs into different draw layers.
    # however it seems like OOT skeletons don't have this ability.
    # Therefore we always use the drawLayerOverride as the draw layer key.
    # This means everything will be saved to one mesh.
    fMesh = fModel.addMesh(vertexGroup, namePrefix, drawLayerOverride, False, bone)

    for material_index, faces in groupFaces.items():
        material = meshObj.material_slots[material_index].material
        checkForF3dMaterialInFaces(meshObj, material)

        fMaterial, texDimensions = saveOrGetF3DMaterial(
            material, fModel, meshObj, drawLayerOverride, convertTextureData
        )

        if fMaterial.useLargeTextures:
            currentGroupIndex = saveMeshWithLargeTexturesByFaces(
                material,
                faces,
                fModel,
                fMesh,
                meshObj,
                drawLayerOverride,
                convertTextureData,
                currentGroupIndex,
                triConverterInfo,
                None,
                None,
                lastMaterialName,
            )
        else:
            currentGroupIndex = saveMeshByFaces(
                material,
                faces,
                fModel,
                fMesh,
                meshObj,
                drawLayerOverride,
                convertTextureData,
                currentGroupIndex,
                triConverterInfo,
                None,
                None,
                lastMaterialName,
            )

        lastMaterialName = material.name if optimize else None

    fModel.endDraw(fMesh, bone)

    return fMesh, hasSkinnedFaces, lastMaterialName
