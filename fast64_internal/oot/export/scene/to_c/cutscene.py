from .....utility import CData
from ....oot_cutscene import ootCutsceneDataToC
from ...classes.scene import OOTScene


def convertCutscenes(outScene: OOTScene):
    """Returns the cutscene data"""
    csData: list[CData] = []
    sceneLayers: list[OOTScene] = [outScene, outScene.childNightHeader, outScene.adultDayHeader, outScene.adultNightHeader]
    sceneLayers.extend(outScene.cutsceneHeaders)

    for i, layer in enumerate(sceneLayers):
        if layer is not None and layer.writeCutscene:
            data = CData()
            if layer.csWriteType == "Embedded":
                data = ootCutsceneDataToC(layer, layer.getCutsceneDataName(i))
            elif layer.csWriteType == "Object":
                data = ootCutsceneDataToC(layer.csWriteObject, layer.csWriteObject.name)
            csData.append(data)

    for extraCs in outScene.extraCutscenes:
        csData.append(ootCutsceneDataToC(extraCs, extraCs.name))

    return csData
