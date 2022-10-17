from os import path as p
from ..exporter.utility import ootGetPath


def ootGetObjectPath(isCustomExport: bool, exportPath: str, folderName: str):
    if isCustomExport:
        filepath = exportPath
    else:
        filepath = p.join(
            ootGetPath(exportPath, isCustomExport, "assets/objects/", folderName, False, False), folderName + ".c"
        )
    return filepath
