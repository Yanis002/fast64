import os, bpy
from ...utility import PluginError, writeFile
from ..data import ootEnumSceneID
from .classes import ExportInfo, OOTScene


def getDrawConfigList(exportPath: str):
    """Returns the list of available draw configs"""
    configNames: list[str] = []
    lines: list[str] = []

    # get every lines until reaching the end of the draw config enum
    try:
        with open(os.path.join(exportPath, "include/z64scene.h")) as fileData:
            for line in fileData:
                if "SceneDrawConfig;" not in line:
                    lines.append(line)
                else:
                    break
    except:
        raise PluginError("ERROR: Can't find z64scene.h!")

    # keep the relevant lines
    for line in reversed(lines):
        if line != "\n":
            if "MAX" not in line and "*/ " in line:
                # split the string a first time to get rid of the comments
                # then split the second element of the list to get rid of the index comment
                # and only keep the config name
                configNames.append(line.split(",")[0].split("*/ ")[1])
        else:
            break

    return list(reversed(configNames))


def getSceneTable(exportPath: str) -> tuple[list[str], str, list[str]]:
    """Read and remove unwanted stuff from ``scene_table.h``"""
    sceneEntries = []
    sceneNames = []
    fileHeader = ""  # the comment at the beginning of the file

    # read the scene table
    try:
        with open(os.path.join(exportPath, "include/tables/scene_table.h")) as fileData:
            # keep the relevant data and do some formatting
            for line in fileData:
                if not line.startswith("// "):
                    if not (line.startswith("/**") or line.startswith(" *")):
                        sceneEntries.append(line[(line.find("(") + 1) :].rstrip(")\n").replace(" ", "").split(","))
                    else:
                        fileHeader += line
                if line.startswith("/* 0x"):
                    startIndex = line.find("SCENE_")
                    sceneNames.append(line[startIndex : line.find(",", startIndex)])
    except FileNotFoundError:
        raise PluginError("ERROR: Can't find scene_table.h!")

    # return the parsed data, the header comment and the scene's names
    return sceneEntries, fileHeader, sceneNames


def getSceneIndex(sceneNames: list[str], sceneName: str):
    """Returns the index (int) of the chosen scene, returns None if ``Custom`` is chosen"""
    if sceneName == "Custom":
        return None

    for scnName in sceneNames:
        if scnName == sceneName:
            return sceneNames.index(scnName)

    # if the scene isn't a custom one and the index wasn't returned
    raise NotImplementedError


def getOriginalIndex(sceneName: str):
    """
    Returns the index of a specific scene defined by which one the user chose
        or by the ``sceneName`` parameter if it's not set to ``None``
    """
    if sceneName is not None and sceneName != "Custom":
        for elem in ootEnumSceneID:
            if elem[0] == sceneName:
                # -1 because the first entry is the ``Custom`` option
                return ootEnumSceneID.index(elem) - 1

    raise PluginError("ERROR: Scene Index not found!")


def getInsertionIndex(sceneNames: list[str], sceneName: str, index: int, mode: str) -> int:
    """Returns the index to know where to insert data"""
    # special case where the scene is "Inside the Great Deku Tree"
    # since it's the first scene simply return 0
    if sceneName == "SCENE_YDAN":
        return 0

    # if index is None this means this is looking for ``original_scene_index - 1``
    # else, this means the table is shifted
    if index is None:
        currentIndex = getOriginalIndex(sceneName)
    else:
        currentIndex = index

    for i in range(len(sceneNames)):
        if sceneNames[i] == ootEnumSceneID[currentIndex][0]:
            # return an index to insert new data
            if mode == "INSERT":
                return i + 1
            # return an index to insert a comment
            elif mode == "EXPORT":
                return i if not sceneName in sceneNames and sceneName != bpy.context.scene.ootSceneOption else i + 1
            # same but don't check for chosen scene
            elif mode == "REMOVE":
                return i if not sceneName in sceneNames else i + 1
            else:
                raise NotImplementedError

    # if the index hasn't been found yet, do it again but decrement the index
    return getInsertionIndex(sceneNames, sceneName, currentIndex - 1, mode)


def getSceneParams(scene: OOTScene, exportInfo: ExportInfo, sceneNames: list[str]):
    """Returns the parameters that needs to be set in ``DEFINE_SCENE()``"""
    # in order to replace the values of ``unk10``, ``unk12`` and basically every parameters from ``DEFINE_SCENE``,
    # you just have to make it return something other than None, not necessarily a string
    sceneIndex = getSceneIndex(sceneNames, bpy.context.scene.ootSceneOption)
    sceneName = sceneTitle = sceneID = sceneUnk10 = sceneUnk12 = None

    # if the index is None then this is a custom scene
    if sceneIndex is None and scene is not None:
        sceneName = scene.getSceneName()
        sceneTitle = "none"
        sceneID = "SCENE_" + (scene.name.upper() if scene is not None else exportInfo.name.upper())
        sceneUnk10 = sceneUnk12 = 0

    return sceneName, sceneTitle, sceneID, sceneUnk10, sceneUnk12, sceneIndex


def sceneTableToC(sceneEntries: list[str], header: str, sceneNames: list[str], scene: OOTScene):
    """Converts the Scene Table to C code"""
    # start the data with the header comment explaining the format of the file
    fileData = header

    # determine if this function is called by 'Remove Scene' or 'Export Scene'
    mode = "EXPORT" if scene is not None else "REMOVE"

    # get the index of the last non-debug scene
    lastNonDebugSceneIdx = getInsertionIndex(sceneNames, "SCENE_GANON_TOU", None, mode)
    lastSceneIdx = getInsertionIndex(sceneNames, "SCENE_TESTROOM", None, mode)

    # add the actual lines with the same formatting
    for sceneEntry in sceneEntries:
        i = sceneEntries.index(sceneEntry)
        # adds the "// Debug-only scenes"
        # if both lastScene indexes are the same values this means there's no debug scene
        if ((i - 1) == lastNonDebugSceneIdx) and (lastSceneIdx != lastNonDebugSceneIdx):
            fileData += "// Debug-only scenes\n"

        # add a comment to show when it's new scenes
        if (i - 1) == lastSceneIdx:
            fileData += "// Added scenes\n"

        fileData += f"/* 0x{i:02X} */ DEFINE_SCENE({', '.join(f'{sceneArg}' for sceneArg in sceneEntry)})\n"

    # return the string containing the file data to write
    return fileData


def modifySceneTable(scene: OOTScene, exportInfo: ExportInfo):
    """Edit the scene table with the new data"""
    exportPath = exportInfo.exportPath
    # the list ``sceneNames`` needs to be synced with ``fileData``
    fileData, header, sceneNames = getSceneTable(exportPath)
    sceneName, sceneTitle, sceneID, sceneUnk10, sceneUnk12, sceneIndex = getSceneParams(scene, exportInfo, sceneNames)
    drawConfigNames = getDrawConfigList(exportPath)

    if scene is None:
        sceneDrawConfig = None
    elif scene.sceneTableEntry.drawConfig < len(drawConfigNames):
        sceneDrawConfig = drawConfigNames[scene.sceneTableEntry.drawConfig]
    else:
        sceneDrawConfig = scene.sceneTableEntry.drawConfig

    # ``DEFINE_SCENE()`` parameters
    sceneParams = [sceneName, sceneTitle, sceneID, sceneDrawConfig, sceneUnk10, sceneUnk12]

    # check if it's a custom scene name
    # sceneIndex can be None and ootSceneOption not "Custom",
    # that means the selected scene has been removed from the table
    # however if the scene variable is not None
    # set it to "INSERT" because we need to insert the scene in the right place
    if sceneIndex is None and bpy.context.scene.ootSceneOption == "Custom":
        mode = "CUSTOM"
    elif sceneIndex is None and scene is not None:
        mode = "INSERT"
    elif sceneIndex is not None:
        mode = "NORMAL"
    else:
        mode = None

    if mode is not None:
        # if so, check if the custom scene already exists in the data
        # if it already exists set mode to NORMAL to consider it like a normal scene
        if mode == "CUSTOM":
            exportName = bpy.context.scene.ootSceneName.lower()
            for i in range(len(fileData)):
                if fileData[i][0] == exportName + "_scene":
                    sceneIndex = i
                    mode = "NORMAL"
                    break
        else:
            exportName = exportInfo.name

        # edit the current data or append new one if we are in a ``Custom`` context
        if mode == "NORMAL":
            for i in range(6):
                if sceneParams[i] is not None and fileData[sceneIndex][i] != sceneParams[i]:
                    fileData[sceneIndex][i] = sceneParams[i]
        elif mode == "CUSTOM":
            sceneNames.append(sceneParams[2])
            fileData.append(sceneParams)
            sceneIndex = len(fileData) - 1
        elif mode == "INSERT":
            # if this the user chose a vanilla scene, removed it and want to export
            # insert the data in the normal location
            # shifted index = vanilla index - (vanilla last scene index - new last scene index)
            index = getInsertionIndex(sceneNames, sceneID, None, mode)
            sceneNames.insert(index, sceneParams[2])
            fileData.insert(index, sceneParams)

    # remove the scene data if scene is None (`Remove Scene` button)
    if scene is None:
        if sceneIndex is not None:
            sceneNames.pop(sceneIndex)
            fileData.pop(sceneIndex)
        else:
            raise PluginError("ERROR: Scene not found in ``scene_table.h``!")

    # write the file with the final data
    writeFile(
        os.path.join(exportPath, "include/tables/scene_table.h"), sceneTableToC(fileData, header, sceneNames, scene)
    )
