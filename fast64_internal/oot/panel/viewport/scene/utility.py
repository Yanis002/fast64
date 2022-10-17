from .....utility import PluginError
from .data import ootSceneIDToName


def sceneNameFromID(sceneID: str):
    if sceneID in ootSceneIDToName:
        return ootSceneIDToName[sceneID]
    else:
        raise PluginError("Cannot find scene ID " + str(sceneID))
