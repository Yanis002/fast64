import bpy
from os import path
from bpy.types import Object
from mathutils import Matrix
from ...f3d.f3d_gbi import ScrollMethod, DLFormat, TextureExportSettings
from ...utility import PluginError, CData, writeCDataSourceOnly, writeCDataHeaderOnly, checkObjectReference
from ..oot_utility import ExportInfo, ootGetPath, ootSceneDirs
from ..oot_model_classes import OOTGfxFormatter
from ..oot_collision import ootCollisionToC
from .room.to_c import convertRoomShapeData, convertRoomModel, convertRoomLayers
from .scene.to_c import convertSceneLayers
from .cutscene.to_c import convertCutsceneToC, getCutsceneIncludes
from .scene_table import modifySceneTable
from .spec import modifySegmentDefinition
from .scene_folder import modifySceneFiles
from .scene import processScene
from .classes.scene import OOTScene
from .classes import OOTSceneC
from .hackeroot.scene_bootup import OOTBootupSceneOptions, setBootupScene


def generateC(outScene: OOTScene, textureExportSettings: TextureExportSettings):
    sceneC = OOTSceneC()
    textureData = outScene.model.to_c(textureExportSettings, OOTGfxFormatter(ScrollMethod.Vertex)).all()

    sceneC.sceneMainC = convertSceneLayers(outScene)
    sceneC.sceneTexturesC = textureData
    sceneC.sceneCollisionC = ootCollisionToC(outScene.collision)
    sceneC.sceneCutscenesC = convertCutsceneToC(outScene)

    for room in outScene.rooms.values():
        name = room.getRoomName()
        sceneC.roomMainC[name] = convertRoomLayers(room)
        sceneC.roomMeshInfoC[name] = convertRoomShapeData(room.mesh)
        sceneC.roomMeshC[name] = convertRoomModel(room, textureExportSettings)

    return sceneC


def ootSceneIncludes(outScene: OOTScene):
    sceneIncludeData = CData()
    includeFiles = [
        "ultra64.h",
        "z64.h",
        "macros.h",
        f"{outScene.getSceneName()}.h",
        "segment_symbols.h",
        "command_macros_base.h",
        "variables.h",
    ]

    sceneIncludeData.source = "\n".join([f'#include "{fileName}"' for fileName in includeFiles]) + "\n\n"
    return sceneIncludeData


def ootCombineSceneFiles(sceneC: OOTSceneC):
    # only used for single file export
    newSceneC = CData()
    newSceneC.append(sceneC.sceneMainC)

    if sceneC.sceneTexturesIsUsed():
        newSceneC.append(sceneC.sceneTexturesC)

    newSceneC.append(sceneC.sceneCollisionC)

    if sceneC.sceneCutscenesIsUsed():
        for i in range(len(sceneC.sceneCutscenesC)):
            newSceneC.append(sceneC.sceneCutscenesC[i])

    return newSceneC


def ootCreateSceneHeader(sceneC: OOTSceneC):
    # writes the scene.h file
    sceneHeader = CData()
    sceneHeader.append(sceneC.sceneMainC)

    if sceneC.sceneTexturesIsUsed():
        sceneHeader.append(sceneC.sceneTexturesC)

    sceneHeader.append(sceneC.sceneCollisionC)

    if sceneC.sceneCutscenesIsUsed():
        for sceneCs in sceneC.sceneCutscenesC:
            sceneHeader.append(sceneCs)

    for roomMainC in sceneC.roomMainC.values():
        sceneHeader.append(roomMainC)

    for roomMeshInfoC in sceneC.roomMeshInfoC.values():
        sceneHeader.append(roomMeshInfoC)

    for roomMeshC in sceneC.roomMeshC.values():
        sceneHeader.append(roomMeshC)

    return sceneHeader


def ootPreprendSceneIncludes(outScene: OOTScene, fileData: CData):
    exportFile = ootSceneIncludes(outScene)
    exportFile.append(fileData)
    return exportFile


def exportScene(
    inSceneObj: Object,
    transformMatrix: Matrix,
    f3dType: str,
    isHWv1: bool,  # is hardware v1
    sceneName: str,
    dlFormat: DLFormat,
    savePNG: bool,
    exportInfo: ExportInfo,
    bootToSceneOptions: OOTBootupSceneOptions,
):

    checkObjectReference(inSceneObj, "Scene object")
    isCustomExport = exportInfo.isCustomExportPath
    exportPath = exportInfo.exportPath

    outScene = processScene(inSceneObj, transformMatrix, f3dType, isHWv1, sceneName, dlFormat, not savePNG)

    exportSubdir = ""
    if exportInfo.customSubPath is not None:
        exportSubdir = exportInfo.customSubPath

    if not isCustomExport and exportInfo.customSubPath is None:
        for sceneSubdir, sceneNames in ootSceneDirs.items():
            if sceneName in sceneNames:
                exportSubdir = sceneSubdir
                break

        if exportSubdir == "":
            raise PluginError(f"Scene folder '{sceneName}' cannot be found in the ootSceneDirs list.")

    levelPath = ootGetPath(exportPath, isCustomExport, exportSubdir, sceneName, True, True)
    sceneC = generateC(outScene, TextureExportSettings(False, savePNG, exportSubdir + sceneName, levelPath))

    if bpy.context.scene.ootSceneSingleFile:
        writeCDataSourceOnly(
            ootPreprendSceneIncludes(outScene, ootCombineSceneFiles(sceneC)),
            path.join(levelPath, outScene.getSceneName() + ".c"),
        )

        for room in outScene.rooms.values():
            roomC = CData()
            roomC.append(sceneC.roomMainC[room.getRoomName()])
            roomC.append(sceneC.roomMeshInfoC[room.getRoomName()])
            roomC.append(sceneC.roomMeshC[room.getRoomName()])
            writeCDataSourceOnly(
                ootPreprendSceneIncludes(outScene, roomC), path.join(levelPath, room.getRoomName() + ".c")
            )
    else:
        # Export the scene segment .c files
        writeCDataSourceOnly(
            ootPreprendSceneIncludes(outScene, sceneC.sceneMainC),
            path.join(levelPath, outScene.getSceneName() + "_main.c"),
        )

        if sceneC.sceneTexturesIsUsed():
            writeCDataSourceOnly(
                ootPreprendSceneIncludes(outScene, sceneC.sceneTexturesC),
                path.join(levelPath, outScene.getSceneName() + "_tex.c"),
            )

        writeCDataSourceOnly(
            ootPreprendSceneIncludes(outScene, sceneC.sceneCollisionC),
            path.join(levelPath, outScene.getSceneName() + "_col.c"),
        )

        if sceneC.sceneCutscenesIsUsed():
            for i, sceneCs in enumerate(sceneC.sceneCutscenesC):
                fileData = getCutsceneIncludes(f"{outScene.getSceneName()}.h")
                fileData.append(sceneCs)
                writeCDataSourceOnly(
                    fileData,
                    path.join(levelPath, f"{outScene.getSceneName()}_cs_{i}.c"),
                )

        # Export the room segment .c files
        for roomName, roomMainC in sceneC.roomMainC.items():
            writeCDataSourceOnly(
                ootPreprendSceneIncludes(outScene, roomMainC), path.join(levelPath, f"{roomName}_main.c")
            )

        for roomName, roomMeshInfoC in sceneC.roomMeshInfoC.items():
            writeCDataSourceOnly(
                ootPreprendSceneIncludes(outScene, roomMeshInfoC), path.join(levelPath, f"{roomName}_model_info.c")
            )

        for roomName, roomMeshC in sceneC.roomMeshC.items():
            writeCDataSourceOnly(
                ootPreprendSceneIncludes(outScene, roomMeshC), path.join(levelPath, f"{roomName}_model.c")
            )

    # Export the scene .h file
    writeCDataHeaderOnly(ootCreateSceneHeader(sceneC), path.join(levelPath, outScene.getSceneName() + ".h"))

    if not isCustomExport:
        # update scene table, spec and remove extra rooms
        # if exporting to decomp
        modifySceneTable(outScene, exportInfo)
        modifySegmentDefinition(outScene, exportInfo, sceneC)
        modifySceneFiles(outScene, exportInfo)

    # HackerOoT
    if bootToSceneOptions is not None and bootToSceneOptions.bootToScene:
        setBootupScene(
            path.join(exportPath, "include/config/config_debug.h")
            if not isCustomExport
            else path.join(levelPath, "config_bootup.h"),
            f"ENTR_{sceneName.upper()}_{bootToSceneOptions.spawnIndex}",
            bootToSceneOptions,
        )
