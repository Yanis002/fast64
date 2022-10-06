from .....utility import CData
from ....oot_cutscene import ootCutsceneDataToC
from ...classes.scene import OOTScene


def ootSceneCutscenesToC(scene: OOTScene):
    """Returns the cutscene data"""
    csData: list[CData] = []
    sceneLayers: list[OOTScene] = [scene, scene.childNightHeader, scene.adultDayHeader, scene.adultNightHeader]
    sceneLayers.extend(scene.cutsceneHeaders)

    for i, layer in enumerate(sceneLayers):
        if layer is not None and layer.writeCutscene:
            data = CData()
            if layer.csWriteType == "Embedded":
                data = ootCutsceneDataToC(layer, layer.getCutsceneDataName(i))
            elif layer.csWriteType == "Object":
                data = ootCutsceneDataToC(layer.csWriteObject, layer.csWriteObject.name)
            csData.append(data)

    for extraCs in scene.extraCutscenes:
        csData.append(ootCutsceneDataToC(extraCs, extraCs.name))

    return csData
