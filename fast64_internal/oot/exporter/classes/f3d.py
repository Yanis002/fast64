from mathutils import Matrix
from bpy.types import Object, Armature
from ....f3d.f3d_gbi import F3D, MTX_SIZE
from ....f3d.f3d_writer import MeshInfo, TriangleConverterInfo


class OOTTriangleConverterInfo(TriangleConverterInfo):
    def __init__(self, obj: Object, armature: Armature, f3d: F3D, transformMatrix: Matrix, meshInfo: MeshInfo):
        TriangleConverterInfo.__init__(self, obj, armature, f3d, transformMatrix, meshInfo)

    def getMatrixAddrFromGroup(self, groupIndex: int):
        return f"0x{(0x0D << 24) + MTX_SIZE * self.vertexGroupInfo.vertexGroupToMatrixIndex[groupIndex]:08X}"
