from ...oot_constants import ootSceneIDToName
from ....utility import PluginError


def sceneNameFromID(sceneID):
    if sceneID in ootSceneIDToName:
        return ootSceneIDToName[sceneID]
    else:
        raise PluginError("Cannot find scene ID " + str(sceneID))
