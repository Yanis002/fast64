import bpy, os, mathutils
from bpy.types import Operator, Mesh
from bpy.ops import object
from bpy.path import abspath
from bpy.utils import register_class, unregister_class
from mathutils import Matrix
from pathlib import Path
from ...utility import CData, PluginError, raisePluginError, writeCData, toAlnum
from ...f3d.f3d_parser import importMeshC, getImportData
from ...f3d.f3d_gbi import DLFormat, F3D, TextureExportSettings, ScrollMethod, get_F3D_GBI
from ...f3d.f3d_writer import TriangleConverterInfo, removeDL, saveStaticModel, getInfoDict
from .properties import Z64_DLImportSettings, Z64_DLExportSettings

# TODO: cleanup
from ...oot.oot_model_classes import OOTF3DContext, ootGetIncludedAssetData
from ...oot.oot_texture_array import ootReadTextureArrays
from ...oot.oot_model_classes import OOTModel, OOTGfxFormatter
from ...oot.oot_f3d_writer import ootReadActorScale, writeTextureArraysNew, writeTextureArraysExisting

from ...z64.utility import (
    OOTObjectCategorizer,
    get_path,
    get_object_path,
    get_z64_scale,
    addIncludeFiles,
    ootCleanupScene,
    ootDuplicateHierarchy,
)


def ootConvertMeshToC(
    originalObj: bpy.types.Object,
    finalTransform: mathutils.Matrix,
    DLFormat: DLFormat,
    saveTextures: bool,
    settings: Z64_DLExportSettings,
):
    folderName = settings.folder
    exportPath = bpy.path.abspath(settings.customPath)
    isCustomExport = settings.isCustom
    drawLayer = settings.drawLayer
    removeVanillaData = settings.removeVanillaData
    name = toAlnum(originalObj.name)
    overlayName = settings.actorOverlayName
    flipbookUses2DArray = settings.flipbookUses2DArray
    flipbookArrayIndex2D = settings.flipbookArrayIndex2D if flipbookUses2DArray else None

    try:
        obj, allObjs = ootDuplicateHierarchy(originalObj, None, False, OOTObjectCategorizer())

        fModel = OOTModel(name, DLFormat, drawLayer)
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
        data.source += '#include "' + folderName + '.h"\n\n'
    else:
        data.source += "\n"

    path = get_path(exportPath, isCustomExport, "assets/objects/", folderName, False, True)
    includeDir = settings.customAssetIncludeDir if settings.isCustom else f"assets/objects/{folderName}"
    exportData = fModel.to_c(
        TextureExportSettings(False, saveTextures, includeDir, path), OOTGfxFormatter(ScrollMethod.Vertex)
    )

    data.append(exportData.all())

    if isCustomExport:
        textureArrayData = writeTextureArraysNew(fModel, flipbookArrayIndex2D)
        data.append(textureArrayData)

    filename = settings.filename if settings.isCustomFilename else name
    writeCData(data, os.path.join(path, filename + ".h"), os.path.join(path, filename + ".c"))

    if not isCustomExport:
        writeTextureArraysExisting(bpy.context.scene.z64_decomp_path, overlayName, False, flipbookArrayIndex2D, fModel)
        addIncludeFiles(folderName, path, name)
        if removeVanillaData:
            headerPath = os.path.join(path, folderName + ".h")
            sourcePath = os.path.join(path, folderName + ".c")
            removeDL(sourcePath, headerPath, name)


class OOT_ImportDL(Operator):
    # set bl_ properties
    bl_idname = "object.oot_import_dl"
    bl_label = "Import DL"
    bl_options = {"REGISTER", "UNDO", "PRESET"}

    # Called on demand (i.e. button press, menu item)
    # Can also be called from operator search menu (Spacebar)
    def execute(self, context):
        obj = None
        if context.mode != "OBJECT":
            object.mode_set(mode="OBJECT")

        try:
            settings: Z64_DLImportSettings = context.scene.fast64.z64.DLImportSettings
            name = settings.name
            folderName = settings.folder
            importPath = Path(settings.customPath).resolve()
            isCustomImport = settings.isCustom
            basePath = (
                Path(bpy.context.scene.z64_decomp_path).resolve() if not isCustomImport else os.path.dirname(importPath)
            )
            removeDoubles = settings.removeDoubles
            importNormals = settings.importNormals
            drawLayer = settings.drawLayer
            overlayName = settings.actorOverlayName
            flipbookUses2DArray = settings.flipbookUses2DArray
            flipbookArrayIndex2D = settings.flipbookArrayIndex2D if flipbookUses2DArray else None

            paths = [get_object_path(isCustomImport, importPath, folderName, True)]
            filedata = getImportData(paths)
            f3dContext = OOTF3DContext(get_F3D_GBI(), [name], basePath)

            scale = get_z64_scale(settings.actorScale)
            if not isCustomImport:
                filedata = ootGetIncludedAssetData(basePath, paths, filedata) + filedata

                if overlayName is not None:
                    ootReadTextureArrays(basePath, overlayName, name, f3dContext, False, flipbookArrayIndex2D)
                if settings.autoDetectActorScale:
                    scale = ootReadActorScale(basePath, overlayName, False)

            obj = importMeshC(
                filedata,
                name,
                scale,
                removeDoubles,
                importNormals,
                drawLayer,
                f3dContext,
            )
            obj.ootActorScale = scale / context.scene.z64_blender_scale

            self.report({"INFO"}, "Success!")
            return {"FINISHED"}

        except Exception as e:
            if context.mode != "OBJECT":
                object.mode_set(mode="OBJECT")
            raisePluginError(self, e)
            return {"CANCELLED"}  # must return a set


class OOT_ExportDL(Operator):
    # set bl_ properties
    bl_idname = "object.oot_export_dl"
    bl_label = "Export DL"
    bl_options = {"REGISTER", "UNDO", "PRESET"}

    # Called on demand (i.e. button press, menu item)
    # Can also be called from operator search menu (Spacebar)
    def execute(self, context):
        obj = None
        if context.mode != "OBJECT":
            object.mode_set(mode="OBJECT")
        if len(context.selected_objects) == 0:
            raise PluginError("Mesh not selected.")
        obj = context.active_object
        if obj.type != "MESH":
            raise PluginError("Mesh not selected.")

        finalTransform = Matrix.Scale(get_z64_scale(obj.ootActorScale), 4)

        try:
            # exportPath, levelName = getPathAndLevel(context.scene.geoCustomExport,
            # 	context.scene.geoExportPath, context.scene.geoLevelName,
            # 	context.scene.geoLevelOption)

            saveTextures = context.scene.saveTextures
            exportSettings = context.scene.fast64.z64.DLExportSettings

            ootConvertMeshToC(
                obj,
                finalTransform,
                DLFormat.Static,
                saveTextures,
                exportSettings,
            )

            self.report({"INFO"}, "Success!")
            return {"FINISHED"}

        except Exception as e:
            if context.mode != "OBJECT":
                object.mode_set(mode="OBJECT")
            raisePluginError(self, e)
            return {"CANCELLED"}  # must return a set


oot_dl_writer_classes = (
    OOT_ImportDL,
    OOT_ExportDL,
)


def f3d_ops_register():
    for cls in oot_dl_writer_classes:
        register_class(cls)


def f3d_ops_unregister():
    for cls in reversed(oot_dl_writer_classes):
        unregister_class(cls)
