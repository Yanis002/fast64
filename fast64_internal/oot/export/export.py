import bpy
from os import path
from bpy.types import Object
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
from .scene import ootConvertScene
from .classes.scene import OOTScene
from .classes import OOTLevelC
from .hackeroot.scene_bootup import OOTBootupSceneOptions, setBootupScene


def ootLevelToC(scene: OOTScene, textureExportSettings: TextureExportSettings):
    levelC = OOTLevelC()
    textureData = scene.model.to_c(textureExportSettings, OOTGfxFormatter(ScrollMethod.Vertex)).all()

    levelC.sceneMainC = ootSceneLayersToC(scene)
    levelC.sceneTexturesC = textureData
    levelC.sceneCollisionC = ootCollisionToC(scene.collision)
    levelC.sceneCutscenesC = ootSceneCutscenesToC(scene)

    for room in scene.rooms.values():
        name = room.roomName()
        levelC.roomMainC[name] = ootRoomLayersToC(room)
        levelC.roomMeshInfoC[name] = ootGetRoomShapeHeaderData(room.mesh)
        levelC.roomMeshC[name] = ootRoomModelToC(room, textureExportSettings)

    return levelC


def ootSceneIncludes(scene: OOTScene):
    sceneIncludeData = CData()
    includeFiles = [
        "ultra64.h",
        "z64.h",
        "macros.h",
        f"{scene.sceneName()}.h",
        "segment_symbols.h",
        "command_macros_base.h",
        "variables.h",
    ]

    if scene.writeCutscene:
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
        for i in range(len(levelC.sceneCutscenesC)):
            sceneHeader.append(levelC.sceneCutscenesC[i])
    for roomName, roomMainC in levelC.roomMainC.items():
        sceneHeader.append(roomMainC)
    for roomName, roomMeshInfoC in levelC.roomMeshInfoC.items():
        sceneHeader.append(roomMeshInfoC)
    for roomName, roomMeshC in levelC.roomMeshC.items():
        sceneHeader.append(roomMeshC)

    return sceneHeader


def ootPreprendSceneIncludes(scene: OOTScene, file: CData):
    exportFile = ootSceneIncludes(scene)
    exportFile.append(file)
    return exportFile


def ootExportSceneToC(
    originalSceneObj: Object,
    transformMatrix,
    f3dType: str,
    isHWv1: bool,
    sceneName: str,
    DLFormat: DLFormat,
    savePNG: bool,
    exportInfo: ExportInfo,
    bootToSceneOptions: OOTBootupSceneOptions,
):

    checkObjectReference(originalSceneObj, "Scene object")
    isCustomExport = exportInfo.isCustomExportPath
    exportPath = exportInfo.exportPath

    scene = ootConvertScene(originalSceneObj, transformMatrix, f3dType, isHWv1, sceneName, DLFormat, not savePNG)

    exportSubdir = ""
    if exportInfo.customSubPath is not None:
        exportSubdir = exportInfo.customSubPath
    if not isCustomExport and exportInfo.customSubPath is None:
        for sceneSubdir, sceneNames in ootSceneDirs.items():
            if sceneName in sceneNames:
                exportSubdir = sceneSubdir
                break
        if exportSubdir == "":
            raise PluginError("Scene folder " + sceneName + " cannot be found in the ootSceneDirs list.")

    levelPath = ootGetPath(exportPath, isCustomExport, exportSubdir, sceneName, True, True)
    levelC = ootLevelToC(scene, TextureExportSettings(False, savePNG, exportSubdir + sceneName, levelPath))

    if bpy.context.scene.ootSceneSingleFile:
        writeCDataSourceOnly(
            ootPreprendSceneIncludes(scene, ootCombineSceneFiles(levelC)),
            path.join(levelPath, scene.sceneName() + ".c"),
        )
        for i in range(len(scene.rooms)):
            roomC = CData()
            roomC.append(levelC.roomMainC[scene.rooms[i].roomName()])
            roomC.append(levelC.roomMeshInfoC[scene.rooms[i].roomName()])
            roomC.append(levelC.roomMeshC[scene.rooms[i].roomName()])
            writeCDataSourceOnly(
                ootPreprendSceneIncludes(scene, roomC), path.join(levelPath, scene.rooms[i].roomName() + ".c")
            )
    else:
        # Export the scene segment .c files
        writeCDataSourceOnly(
            ootPreprendSceneIncludes(scene, levelC.sceneMainC), path.join(levelPath, scene.sceneName() + "_main.c")
        )
        if levelC.sceneTexturesIsUsed():
            writeCDataSourceOnly(
                ootPreprendSceneIncludes(scene, levelC.sceneTexturesC),
                path.join(levelPath, scene.sceneName() + "_tex.c"),
            )
        writeCDataSourceOnly(
            ootPreprendSceneIncludes(scene, levelC.sceneCollisionC),
            path.join(levelPath, scene.sceneName() + "_col.c"),
        )
        if levelC.sceneCutscenesIsUsed():
            for i in range(len(levelC.sceneCutscenesC)):
                writeCDataSourceOnly(
                    ootPreprendSceneIncludes(scene, levelC.sceneCutscenesC[i]),
                    path.join(levelPath, scene.sceneName() + "_cs_" + str(i) + ".c"),
                )

        # Export the room segment .c files
        for roomName, roomMainC in levelC.roomMainC.items():
            writeCDataSourceOnly(ootPreprendSceneIncludes(scene, roomMainC), path.join(levelPath, roomName + "_main.c"))
        for roomName, roomMeshInfoC in levelC.roomMeshInfoC.items():
            writeCDataSourceOnly(
                ootPreprendSceneIncludes(scene, roomMeshInfoC), path.join(levelPath, roomName + "_model_info.c")
            )
        for roomName, roomMeshC in levelC.roomMeshC.items():
            writeCDataSourceOnly(
                ootPreprendSceneIncludes(scene, roomMeshC), path.join(levelPath, roomName + "_model.c")
            )

    # Export the scene .h file
    writeCDataHeaderOnly(ootCreateSceneHeader(levelC), path.join(levelPath, scene.sceneName() + ".h"))

    if not isCustomExport:
        # update scene table, spec remove extra ro
        modifySceneTable(scene, exportInfo)
        modifySegmentDefinition(scene, exportInfo, levelC)
        modifySceneFiles(scene, exportInfo)

    if bootToSceneOptions is not None and bootToSceneOptions.bootToScene:
        setBootupScene(
            path.join(exportPath, "include/config/config_debug.h")
            if not isCustomExport
            else path.join(levelPath, "config_bootup.h"),
            "ENTR_" + sceneName.upper() + "_" + str(bootToSceneOptions.spawnIndex),
            bootToSceneOptions,
        )
