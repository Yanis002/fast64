from ....utility import CData


class OOTSceneC:
    def __init__(self):
        # Main header file for both the scene and room(s)
        self.header = CData()

        # Files for the scene segment
        self.sceneMainC = CData()
        self.sceneTexturesC = CData()
        self.sceneCollisionC = CData()
        self.sceneCutscenesC: list[CData] = []

        # Files for room segments
        self.roomMainC: dict[str, CData] = {}
        self.roomMeshInfoC: dict[str, CData] = {}
        self.roomMeshC: dict[str, CData] = {}

    def sceneTexturesIsUsed(self):
        return len(self.sceneTexturesC.source) > 0

    def sceneCutscenesIsUsed(self):
        return len(self.sceneCutscenesC) > 0
