from ....utility import CData


class OOTLevelC:
    def __init__(self):
        # Main header file for both the scene and room(s)
        self.header = CData()

        # Files for the scene segment
        self.sceneMainC = CData()
        self.sceneTexturesC = CData()
        self.sceneCollisionC = CData()
        self.sceneCutscenesC = []

        # Files for room segments
        self.roomMainC = {}
        self.roomMeshInfoC = {}
        self.roomMeshC = {}

    def sceneTexturesIsUsed(self):
        return len(self.sceneTexturesC.source) > 0

    def sceneCutscenesIsUsed(self):
        return len(self.sceneCutscenesC) > 0
