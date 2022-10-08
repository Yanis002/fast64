from bpy.types import Object
from bpy.path import abspath
from mathutils import Matrix
from os import path
from .....f3d.f3d_gbi import DLFormat, TextureExportSettings, ScrollMethod
from ....model import OOTModel, OOTGfxFormatter
from ....panel.viewport.skeleton.classes import OOTSkeletonExportSettings
from ....oot_utility import ootGetPath, addIncludeFiles
from ....skeleton.utility import ootGetSkeleton, ootGetLimbs, ootGetLimb
from ...skeleton import convertArmatureToSkel

from .....utility import (
    PluginError,
    CData,
    writeCData,
    toAlnum,
    writeFile,
    readFile,
    getDeclaration,
)


def convertArmatureToSkelWithMesh(
    originalArmatureObj: Object,
    convertTransformMatrix: Matrix,
    fModel: OOTModel,
    name: str,
    convertTextureData: bool,
    drawLayer: str,
    optimize: bool,
):
    return convertArmatureToSkel(
        originalArmatureObj, convertTransformMatrix, fModel, name, convertTextureData, False, drawLayer, optimize
    )


def removeSkeleton(filePath: str, objectName: str, skeletonName: str):
    headerPath = path.join(filePath, objectName + ".h")
    sourcePath = path.join(filePath, objectName + ".c")

    skeletonDataC = readFile(sourcePath)
    originalDataC = skeletonDataC

    skeletonDataH = readFile(headerPath)
    originalDataH = skeletonDataH

    matchResult = ootGetSkeleton(skeletonDataC, skeletonName, True)

    if matchResult is not None:
        skeletonDataC = skeletonDataC[: matchResult.start(0)] + skeletonDataC[matchResult.end(0) :]
        limbsName = matchResult.group(2)

        headerMatch = getDeclaration(skeletonDataH, skeletonName)

        if headerMatch is not None:
            skeletonDataH = skeletonDataH[: headerMatch.start(0)] + skeletonDataH[headerMatch.end(0) :]

        matchResult = ootGetLimbs(skeletonDataC, limbsName, True)

        if matchResult is not None:
            skeletonDataC = skeletonDataC[: matchResult.start(0)] + skeletonDataC[matchResult.end(0) :]
            limbsData = matchResult.group(2)
            limbList = [entry.strip()[1:] for entry in limbsData.split(",")]

            headerMatch = getDeclaration(skeletonDataH, limbsName)
            if headerMatch is not None:
                skeletonDataH = skeletonDataH[: headerMatch.start(0)] + skeletonDataH[headerMatch.end(0) :]

            for limb in limbList:
                matchResult = ootGetLimb(skeletonDataC, limb, True)
                if matchResult is not None:
                    skeletonDataC = skeletonDataC[: matchResult.start(0)] + skeletonDataC[matchResult.end(0) :]

                headerMatch = getDeclaration(skeletonDataH, limb)

                if headerMatch is not None:
                    skeletonDataH = skeletonDataH[: headerMatch.start(0)] + skeletonDataH[headerMatch.end(0) :]

            if skeletonDataC != originalDataC:
                writeFile(sourcePath, skeletonDataC)

            if skeletonDataH != originalDataH:
                writeFile(headerPath, skeletonDataH)


def ootConvertArmatureToC(
    originalArmatureObj: Object,
    convertTransformMatrix: Matrix,
    f3dType: str,
    isHWv1: bool,
    DLFormat: DLFormat,
    savePNG: bool,
    drawLayer: str,
    settings: OOTSkeletonExportSettings,
):
    folderName = settings.folder
    exportPath = abspath(settings.customPath)
    isCustomExport = settings.isCustom
    removeVanillaData = settings.removeVanillaData
    skeletonName = toAlnum(settings.name)
    optimize = settings.optimize

    fModel = OOTModel(f3dType, isHWv1, skeletonName, DLFormat, drawLayer)
    skeleton, fModel = convertArmatureToSkelWithMesh(
        originalArmatureObj, convertTransformMatrix, fModel, skeletonName, not savePNG, drawLayer, optimize
    )

    if originalArmatureObj.ootFarLOD is not None:
        lodSkeleton, fModel = convertArmatureToSkelWithMesh(
            originalArmatureObj.ootFarLOD,
            convertTransformMatrix,
            fModel,
            skeletonName + "_lod",
            not savePNG,
            drawLayer,
            optimize,
        )

        skeleton.hasLOD = True
        limbList = skeleton.createLimbList()
        lodLimbList = lodSkeleton.createLimbList()

        if len(limbList) != len(lodLimbList):
            raise PluginError(
                originalArmatureObj.name
                + " cannot use "
                + originalArmatureObj.ootFarLOD.name
                + "as LOD because they do not have the same bone structure."
            )

        for i in range(len(limbList)):
            limbList[i].lodDL = lodLimbList[i].DL
            limbList[i].isFlex |= lodLimbList[i].isFlex

    data = CData()
    data.source += '#include "ultra64.h"\n#include "global.h"\n'

    if not isCustomExport:
        data.source += f'#include "{folderName}.h"\n'

    data.source += "\n"
    path = ootGetPath(exportPath, isCustomExport, "assets/objects/", folderName, False, True)
    includeDir = settings.customAssetIncludeDir if settings.isCustom else f"assets/objects/{folderName}"

    exportData = fModel.to_c(
        TextureExportSettings(False, savePNG, includeDir, path), OOTGfxFormatter(ScrollMethod.Vertex)
    )

    skeletonC = skeleton.toC()
    data.append(exportData.all())
    data.append(skeletonC)

    name = skeletonName if isCustomExport else ""
    writeCData(data, path + f"{name}.h", path + f"{name}.c")

    if not isCustomExport:
        addIncludeFiles(folderName, path, skeletonName)
        if removeVanillaData:
            removeSkeleton(path, folderName, skeletonName)
