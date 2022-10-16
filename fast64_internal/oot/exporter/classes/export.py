from bpy.types import Mesh, Object


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
