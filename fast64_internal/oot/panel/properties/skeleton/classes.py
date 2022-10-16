from .....f3d.f3d_writer import VertexGroupInfo


class OOTVertexGroupInfo(VertexGroupInfo):
    def __init__(self):
        self.vertexGroupToMatrixIndex = {}
        VertexGroupInfo.__init__(self)
