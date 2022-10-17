from bpy.types import Mesh, Object
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


class OOTCommonCommands:
    def getAltLayersListCmd(self, altLayerListName: str):
        """Returns the alternate scene layer command"""
        return f"SCENE_CMD_ALTERNATE_HEADER_LIST({altLayerListName})"

    def getEndMarkerCmd(self):
        """Returns the end marker command, common to scenes and rooms"""
        # ``SCENE_CMD_END`` defines the end of scene commands
        return "SCENE_CMD_END(),\n"


class ExportInfo:
    def __init__(self, isCustomExport: bool, exportPath: str, customSubPath: str, name: str):
        self.isCustomExportPath = isCustomExport
        self.exportPath = exportPath
        self.customSubPath = customSubPath
        self.name = name


class OOTObjectCategorizer:
    def __init__(self):
        self.sceneObj = None
        self.roomObjs = []
        self.actors = []
        self.transitionActors = []
        self.meshes = []
        self.entrances = []
        self.waterBoxes = []

    def sortObjects(self, allObjs: list[Object]):
        for obj in allObjs:
            if obj.data is None:
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
            elif isinstance(obj.data, Mesh):
                self.meshes.append(obj)


class BoxEmpty:
    def __init__(self, position: list[int], scale: list[int], emptyScale: float):
        # The scale ordering is due to the fact that scaling happens AFTER rotation.
        # Thus the translation uses Y-up, while the scale uses Z-up.
        self.low = (position[0] - scale[0] * emptyScale, position[2] - scale[1] * emptyScale)
        self.high = (position[0] + scale[0] * emptyScale, position[2] + scale[1] * emptyScale)
        self.height = position[1] + scale[2] * emptyScale

        self.low = [round(value) for value in self.low]
        self.high = [round(value) for value in self.high]
        self.height = round(self.height)


class CullGroup:
    def __init__(self, position: list[int], scale: list[int], emptyScale: float):
        self.position = [round(field) for field in position]
        self.cullDepth = abs(round(scale[0] * emptyScale))
