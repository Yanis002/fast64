import bpy
from os import path
from bpy.types import Object
from mathutils import Matrix
from ...f3d.f3d_gbi import ScrollMethod, DLFormat, TextureExportSettings
from ...utility import PluginError, CData, writeCDataSourceOnly, writeCDataHeaderOnly, checkObjectReference
from ..oot_utility import ExportInfo, ootGetPath, ootSceneDirs
from ..oot_model_classes import OOTGfxFormatter
from ..oot_collision import ootCollisionToC
from ..export.room_writer.oot_room_shape_to_c import ootGetRoomShapeHeaderData, ootRoomModelToC
from ..export.room_writer.oot_room_layer_to_c import ootRoomLayersToC
from ..export.scene_writer.oot_cutscene_to_c import ootSceneCutscenesToC
from ..export.scene_writer.oot_scene_layer_to_c import ootSceneLayersToC
from .other.scene_table import modifySceneTable
from .other.spec import modifySegmentDefinition
from .other.scene_folder import modifySceneFiles
from .scene import processScene
from .classes.scene import OOTScene
from .classes import OOTLevelC
from .hackeroot.scene_bootup import OOTBootupSceneOptions, setBootupScene


def ootLevelToC(outScene: OOTScene, textureExportSettings: TextureExportSettings):
    levelC = OOTLevelC()
    textureData = outScene.model.to_c(textureExportSettings, OOTGfxFormatter(ScrollMethod.Vertex)).all()

    levelC.sceneMainC = ootSceneLayersToC(outScene)
    levelC.sceneTexturesC = textureData
    levelC.sceneCollisionC = ootCollisionToC(outScene.collision)
    levelC.sceneCutscenesC = ootSceneCutscenesToC(outScene)

    for room in outScene.rooms.values():
        name = room.roomName()
        levelC.roomMainC[name] = ootRoomLayersToC(room)
        levelC.roomMeshInfoC[name] = ootGetRoomShapeHeaderData(room.mesh)
        levelC.roomMeshC[name] = ootRoomModelToC(room, textureExportSettings)

    return levelC


def ootSceneIncludes(outScene: OOTScene):
    sceneIncludeData = CData()
    includeFiles = [
        "ultra64.h",
        "z64.h",
        "macros.h",
        f"{outScene.sceneName()}.h",
        "segment_symbols.h",
        "command_macros_base.h",
        "variables.h",
    ]

    if outScene.writeCutscene:
        includeFiles.append("z64cutscene_commands.h")

    sceneIncludeData.source = "\n".join([f'#include "{fileName}"' for fileName in includeFiles]) + "\n\n"
    return sceneIncludeData


def ootCombineSceneFiles(levelC: OOTLevelC):
    # only used for single file export
    sceneC = CData()
    sceneC.append(levelC.sceneMainC)

    if levelC.sceneTexturesIsUsed():
        sceneC.append(levelC.sceneTexturesC)

    sceneC.append(levelC.sceneCollisionC)

    if levelC.sceneCutscenesIsUsed():
        for i in range(len(levelC.sceneCutscenesC)):
            sceneC.append(levelC.sceneCutscenesC[i])

    return sceneC


def ootCreateSceneHeader(levelC: OOTLevelC):
    # writes the scene.h file
    sceneHeader = CData()
    sceneHeader.append(levelC.sceneMainC)

    if levelC.sceneTexturesIsUsed():
        sceneHeader.append(levelC.sceneTexturesC)

    sceneHeader.append(levelC.sceneCollisionC)

    if levelC.sceneCutscenesIsUsed():
        for sceneCs in levelC.sceneCutscenesC:
            sceneHeader.append(sceneCs)

    for roomMainC in levelC.roomMainC.values():
        sceneHeader.append(roomMainC)

    for roomMeshInfoC in levelC.roomMeshInfoC.values():
        sceneHeader.append(roomMeshInfoC)

    for roomMeshC in levelC.roomMeshC.values():
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
    levelC = ootLevelToC(outScene, TextureExportSettings(False, savePNG, exportSubdir + sceneName, levelPath))

    if bpy.context.scene.ootSceneSingleFile:
        writeCDataSourceOnly(
            ootPreprendSceneIncludes(outScene, ootCombineSceneFiles(levelC)),
            path.join(levelPath, outScene.sceneName() + ".c"),
        )

        for room in outScene.rooms:
            roomC = CData()
            roomC.append(levelC.roomMainC[room.roomName()])
            roomC.append(levelC.roomMeshInfoC[room.roomName()])
            roomC.append(levelC.roomMeshC[room.roomName()])
            writeCDataSourceOnly(
                ootPreprendSceneIncludes(outScene, roomC), path.join(levelPath, room.roomName() + ".c")
            )
    else:
        # Export the scene segment .c files
        writeCDataSourceOnly(
            ootPreprendSceneIncludes(outScene, levelC.sceneMainC), path.join(levelPath, outScene.sceneName() + "_main.c")
        )

        if levelC.sceneTexturesIsUsed():
            writeCDataSourceOnly(
                ootPreprendSceneIncludes(outScene, levelC.sceneTexturesC),
                path.join(levelPath, outScene.sceneName() + "_tex.c"),
            )

        writeCDataSourceOnly(
            ootPreprendSceneIncludes(outScene, levelC.sceneCollisionC),
            path.join(levelPath, outScene.sceneName() + "_col.c"),
        )

        if levelC.sceneCutscenesIsUsed():
            for i, sceneCs in enumerate(levelC.sceneCutscenesC):
                writeCDataSourceOnly(
                    ootPreprendSceneIncludes(outScene, sceneCs),
                    path.join(levelPath, f"{outScene.sceneName()}_cs_{i}.c"),
                )

        # Export the room segment .c files
        for roomName, roomMainC in levelC.roomMainC.items():
            writeCDataSourceOnly(ootPreprendSceneIncludes(outScene, roomMainC), path.join(levelPath,  f"{roomName}_main.c"))

        for roomName, roomMeshInfoC in levelC.roomMeshInfoC.items():
            writeCDataSourceOnly(
                ootPreprendSceneIncludes(outScene, roomMeshInfoC), path.join(levelPath,  f"{roomName}_model_info.c")
            )

        for roomName, roomMeshC in levelC.roomMeshC.items():
            writeCDataSourceOnly(
                ootPreprendSceneIncludes(outScene, roomMeshC), path.join(levelPath,  f"{roomName}_model.c")
            )

    # Export the scene .h file
    writeCDataHeaderOnly(ootCreateSceneHeader(levelC), path.join(levelPath, outScene.sceneName() + ".h"))

    if not isCustomExport:
        # update scene table, spec and remove extra rooms
        # if exporting to decomp
        modifySceneTable(outScene, exportInfo)
        modifySegmentDefinition(outScene, exportInfo, levelC)
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
