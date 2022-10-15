from os import path as p
from mathutils import Matrix
from bpy.types import Object
from bpy.path import abspath
from .....utility import CData, writeCData, toAlnum
from .....f3d.f3d_gbi import DLFormat, TextureExportSettings, ScrollMethod
from .....f3d.f3d_writer import TriangleConverterInfo, removeDL, saveStaticModel, getInfoDict
from ....panel.viewport.display_list.classes import OOTDLExportSettings
from ....model.classes import OOTModel, OOTGfxFormatter
from ...utility import addIncludeFiles
from ...classes.export import OOTObjectCategorizer

from ...utility import (
    ootDuplicateHierarchy,
    ootCleanupScene,
    ootGetPath,
)


def ootConvertMeshToC(
    originalObj: Object,
    finalTransform: Matrix,
    f3dType: str,
    isHWv1: bool,
    DLFormat: DLFormat,
    saveTextures: bool,
    settings: OOTDLExportSettings,
):
    folderName = settings.folder
    exportPath = abspath(settings.customPath)
    isCustomExport = settings.isCustom
    drawLayer = settings.drawLayer
    removeVanillaData = settings.removeVanillaData
    name = toAlnum(settings.name)

    try:
        obj, allObjs = ootDuplicateHierarchy(originalObj, None, False, OOTObjectCategorizer())

        fModel = OOTModel(f3dType, isHWv1, name, DLFormat, drawLayer)
        triConverterInfo = TriangleConverterInfo(obj, None, fModel.f3d, finalTransform, getInfoDict(obj))

        fMeshes = saveStaticModel(
            triConverterInfo, fModel, obj, finalTransform, fModel.name, not saveTextures, False, "oot"
        )

        # Since we provide a draw layer override, there should only be one fMesh.
        for drawLayer, fMesh in fMeshes.items():
            fMesh.draw.name = name

        ootCleanupScene(originalObj, allObjs)

    except Exception as e:
        ootCleanupScene(originalObj, allObjs)
        raise Exception(str(e))

    data = CData()
    data.source += '#include "ultra64.h"\n#include "global.h"\n'

    if not isCustomExport:
        data.source += f'#include "{folderName}.h"\n\n'
    else:
        data.source += "\n"

    path = ootGetPath(exportPath, isCustomExport, "assets/objects/", folderName, False, True)
    includeDir = settings.customAssetIncludeDir if settings.isCustom else f"assets/objects/{folderName}"
    exportData = fModel.to_c(
        TextureExportSettings(False, saveTextures, includeDir, path), OOTGfxFormatter(ScrollMethod.Vertex)
    )

    data.append(exportData.all())
    writeCData(data, p.join(path, f"{name}.h"), p.join(path, f"{name}.c"))

    if not isCustomExport:
        addIncludeFiles(folderName, path, name)

        if removeVanillaData:
            headerPath = p.join(path, f"{folderName}.h")
            sourcePath = p.join(path, f"{folderName}.c")
            removeDL(sourcePath, headerPath, name)
