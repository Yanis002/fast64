import bpy
from bpy.types import Object
from os import path as p
from mathutils import Matrix
from .....utility import writeCData
from ....oot_utility import ootGetPath, addIncludeFiles, checkEmptyName
from ..export import ootExportAnimationCommon


def exportAnimationC(armatureObj: Object, exportPath: str, isCustomExport: bool, folderName: str, skeletonName: str):
    checkEmptyName(folderName)
    checkEmptyName(skeletonName)

    convertTransformMatrix = (
        Matrix.Scale(bpy.context.scene.ootActorBlenderScale, 4) @ Matrix.Diagonal(armatureObj.scale).to_4x4()
    )

    ootAnim = ootExportAnimationCommon(armatureObj, convertTransformMatrix, skeletonName)
    ootAnimC = ootAnim.toC()
    path = ootGetPath(exportPath, isCustomExport, "assets/objects/", folderName, False, False)
    writeCData(ootAnimC, p.join(path, ootAnim.name + ".h"), p.join(path, ootAnim.name + ".c"))

    if not isCustomExport:
        addIncludeFiles(folderName, path, ootAnim.name)
