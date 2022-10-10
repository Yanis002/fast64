from mathutils import Matrix
from os import path as p
from bpy.types import Object, Context
from .....utility import CData, hideObjsInList, unhideAllAndGetHiddenList, writeCData
from ...classes.collision import OOTCameraData, OOTCameraPosData, OOTCollision, OOTCollisionPolygon, OOTWaterBox
from ..export import exportCollisionCommon

from ....oot_utility import (
    OOTObjectCategorizer,
    addIncludeFiles,
    indent,
    ootCleanupScene,
    ootDuplicateHierarchy,
    ootGetPath,
)


def ootCollisionPolygonToC(
    polygon: OOTCollisionPolygon,
    ignoreCamera: bool,
    ignoreActor: bool,
    ignoreProjectile: bool,
    enableConveyor: bool,
    polygonTypeIndex: int,
):
    vtxData = [
        polygon.convertShort02(ignoreCamera, ignoreActor, ignoreProjectile),
        polygon.convertShort04(enableConveyor),
        polygon.convertShort06(),
    ]

    return (
        (indent + "{\n")
        + (indent * 2 + f"0x{polygonTypeIndex:04X},\n")
        + (indent * 2 + "{ " + ", ".join([f"0x{curData:04X}" for curData in vtxData]) + " },\n")
        + (indent * 2 + "{ " + ", ".join([f"COLPOLY_SNORMAL({normal})" for normal in polygon.normal]) + " },\n")
        + (indent * 2 + f"0x{polygon.distance:04X}\n")
        + (indent + "},\n")
    )


def ootWaterBoxToC(waterBox: OOTWaterBox):
    return (
        ("{ " + f"{waterBox.low[0]}, {waterBox.height}, {waterBox.low[1]}, ")
        + f"{waterBox.high[0] - waterBox.low[0]}, {waterBox.high[1] - waterBox.low[1]}, "
        + (f"{waterBox.propertyData()}" + " },\n")
    )


def ootCameraPosToC(camPos: OOTCameraPosData):
    return (
        indent
        + "{ "
        + ", ".join([f"{pos}" for pos in camPos.position] + " }, ")
        + "{ "
        + ", ".join([f"0x{rot:04X}" for rot in camPos.rotation] + " }, ")
        + "{ "
        + f"{camPos.fov}, {camPos.jfifID}, {camPos.unknown}"
        + " },\n"
    )


def ootCameraEntryToC(camPos: OOTCameraPosData, camData: OOTCameraData, camPosIndex: int):
    count = "3" if camPos.hasPositionData else "0"
    posPtr = f"&{camData.camPositionsName()}[{camPosIndex}]" if camPos.hasPositionData else "NULL"
    return "{ " + f"{camPos.camSType}, {count}, {posPtr}"


def ootCameraDataToC(camData: OOTCameraData):
    camPosData = CData()
    posC = CData()
    camC = CData()
    exportPosData = False

    if len(camData.camPosDict) > 0:
        camDataName = f"BgCamInfo {camData.camDataName()}[{len(camData.camPosDict)}]"
        posDataName = f"Vec3s {camData.camPositionsName()}[{len(camData.camPosDict) * 3}]"

        # .h
        camC.header = f"extern {camDataName};\n"
        posC.header = f"extern {posDataName};\n"

        # .c
        camC.source = camDataName + " = {\n"
        posC.source = posDataName + " = {\n"

        camPosIndex = 0
        for i in range(len(camData.camPosDict)):
            camC.source += "\t" + ootCameraEntryToC(camData.camPosDict[i], camData, camPosIndex) + ",\n"

            if camData.camPosDict[i].hasPositionData:
                posC.source += ootCameraPosToC(camData.camPosDict[i])
                camPosIndex += 3
                exportPosData = True

        posC.source += "};\n\n"
        camC.source += "};\n\n"

    if exportPosData:
        camPosData.append(posC)

    camPosData.append(camC)
    return camPosData


def ootCollisionToC(collision: OOTCollision):
    colData = ootCameraDataToC(collision.cameraData)

    if len(collision.polygonGroups) > 0:
        polygonTypesName = collision.polygonTypesName()
        polygonsName = collision.polygonsName()
        surfaceName = f"SurfaceType {polygonTypesName}[]"
        collisionName = f"CollisionPoly {polygonsName}[]"

        colData.header += f"extern {surfaceName};\n"
        colData.header += f"extern {collisionName};\n"

        polygonTypeC = surfaceName + " = {\n"
        polygonC = collisionName + " = {\n"

        polygonIndex = 0
        for polygonType, polygons in collision.polygonGroups.items():
            polygonTypeC += (
                indent + "{ " + f"0x{polygonType.convertHigh():08X}, 0x{polygonType.convertLow():08X}" + " },\n"
            )

            for polygon in polygons:
                polygonC += ootCollisionPolygonToC(
                    polygon,
                    polygonType.ignoreCameraCollision,
                    polygonType.ignoreActorCollision,
                    polygonType.ignoreProjectileCollision,
                    polygonType.enableConveyor,
                    polygonIndex,
                )
            polygonIndex += 1
        polygonTypeC += "};\n\n"
        polygonC += "};\n\n"

        colData.source += polygonTypeC + polygonC
    else:
        polygonTypesName = polygonsName = "NULL"

    if len(collision.vertices) > 0:
        colData.header += f"extern Vec3s {collision.verticesName()}[{len(collision.vertices)}];\n"
        colData.source += f"Vec3s {collision.verticesName()}[{len(collision.vertices)}]" + " = {\n"

        for vertex in collision.vertices:
            colData.source += indent + "{ " + ", ".join([f"{pos}" for pos in vertex.position]) + " },\n"

        colData.source += "};\n\n"
        collisionVerticesName = collision.verticesName()
    else:
        collisionVerticesName = "NULL"

    if len(collision.waterBoxes) > 0:
        colData.header += f"extern WaterBox {collision.waterBoxesName()}[];\n"
        colData.source += f"WaterBox {collision.waterBoxesName()}" + "[] = {\n"

        for waterBox in collision.waterBoxes:
            colData.source += indent + ootWaterBoxToC(waterBox)

        colData.source += "};\n\n"
        waterBoxesName = collision.waterBoxesName()
    else:
        waterBoxesName = "NULL"

    if len(collision.cameraData.camPosDict) > 0:
        camDataName = f"&{collision.camDataName()}"
    else:
        camDataName = "NULL"

    colData.header += f"extern CollisionHeader {collision.headerName()}" + ";\n"
    colData.source += f"CollisionHeader {collision.headerName()}" + " = {\n"

    if len(collision.bounds) == 2:
        # x, y, z for min and max bounds
        colData.source += (
            indent
            + "{ "
            + ", ".join([f"{minPos}" for minPos in collision.bounds[0]])
            + " },\n"
            + indent
            + "{ "
            + ", ".join([f"{maxPos}" for maxPos in collision.bounds[1]])
            + " },\n"
        )
    else:
        colData.source += "{ 0, 0, 0 },\n" + indent + "{ 0, 0, 0 },\n"

    colData.source += (
        indent
        + f"{len(collision.vertices)}, {collisionVerticesName},\n"
        + indent
        + f"{collision.polygonCount()}, {polygonsName},\n"
        + indent
        + f"{polygonTypesName},\n"
        + indent
        + f"{camDataName},\n"
        + indent
        + f"{len(collision.waterBoxes)}, {waterBoxesName}\n"
        + "};\n\n"
    )

    return colData


def exportCollisionToC(
    context: Context,
    originalObj: Object,
    transformMatrix: Matrix,
    includeChildren: bool,
    name: str,
    isCustomExport: bool,
    folderName: str,
    exportPath: str,
):
    collision = OOTCollision(name)
    collision.cameraData = OOTCameraData(name)

    if context.scene.exportHiddenGeometry:
        hiddenObjs = unhideAllAndGetHiddenList(context.scene)

    # Don't remove ignore_render, as we want to resuse this for collision
    obj, allObjs = ootDuplicateHierarchy(originalObj, None, True, OOTObjectCategorizer())

    if context.scene.exportHiddenGeometry:
        hideObjsInList(hiddenObjs)

    try:
        exportCollisionCommon(collision, obj, transformMatrix, includeChildren)
        ootCleanupScene(originalObj, allObjs)
    except Exception as e:
        ootCleanupScene(originalObj, allObjs)
        raise Exception(str(e))

    collisionC = ootCollisionToC(collision)

    colData = CData()
    colData.source += '#include "ultra64.h"\n#include "z64.h"\n#include "macros.h"\n'

    if not isCustomExport:
        colData.source += f'#include "{folderName}.h"\n\n'
    else:
        colData.source += "\n"

    colData.append(collisionC)

    path = ootGetPath(exportPath, isCustomExport, "assets/objects/", folderName, False, False)
    writeCData(colData, p.join(path, name + ".h"), p.join(path, name + ".c"))

    if not isCustomExport:
        addIncludeFiles(folderName, path, name)
