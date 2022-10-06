from .....f3d.f3d_gbi import ScrollMethod, TextureExportSettings
from .....utility import CData, PluginError
from ....oot_utility import indent
from ....oot_model_classes import OOTGfxFormatter
from ...classes.room import OOTRoom, OOTRoomMeshGroup, OOTRoomMesh


def getRoomShapeEntry(meshEntry: OOTRoomMeshGroup, roomShape: str):
    """Returns a single room shape entry"""
    opaqueName = meshEntry.DLGroup.opaque.name if meshEntry.DLGroup.opaque is not None else "NULL"
    transparentName = meshEntry.DLGroup.transparent.name if meshEntry.DLGroup.transparent is not None else "NULL"
    roomShapeEntry = "{ "

    if roomShape == "ROOM_SHAPE_TYPE_CULLABLE":
        roomShapeEntry += (
            ("{ " + ", ".join([f"{pos}" for pos in meshEntry.cullGroup.position]) + "}, ")
            + f"{meshEntry.cullGroup.cullDepth}, "
        )
    elif roomShape == "ROOM_SHAPE_TYPE_IMAGE":
        raise PluginError("ERROR: Pre-Rendered rooms not supported.")

    return roomShapeEntry + f"{opaqueName}, {transparentName}" + " }\n"


def getRoomShapeEntries(mesh: OOTRoomMesh):
    """Returns the room shape entries array"""
    roomShapeEntryData = CData()
    roomShapeEntryStructs = {
        "ROOM_SHAPE_TYPE_NORMAL": "RoomShapeDListsEntry",
        "ROOM_SHAPE_TYPE_CULLABLE": "RoomShapeCullableEntry",
    }
    roomShapeEntryName = f"{roomShapeEntryStructs[mesh.roomShape]} {mesh.getEntriesName()}[{len(mesh.meshEntries)}]"

    # .h
    roomShapeEntryData.header = f"extern {roomShapeEntryName};\n"

    # .c
    roomShapeEntryData.source = (
        (roomShapeEntryName + " = {\n")
        + " },\n".join([indent + getRoomShapeEntry(entry, mesh.roomShape) for entry in mesh.meshEntries])
        + "};\n\n"
    )

    return roomShapeEntryData


def convertRoomShapeData(mesh: OOTRoomMesh):
    """Returns the room shape header and data"""
    roomShapeData = CData()
    roomShapeStructs = {
        "ROOM_SHAPE_TYPE_NORMAL": "RoomShapeNormal",
        "ROOM_SHAPE_TYPE_CULLABLE": "RoomShapeCullable",
    }
    roomShapeName = f"{roomShapeStructs[mesh.roomShape]} {mesh.getHeaderName()}"
    roomShapeEntryName = mesh.getEntriesName()
    roomShapeArrayCount = f"ARRAY_COUNT({roomShapeEntryName})"

    # .h
    roomShapeData.header = f"extern {roomShapeName};\n"

    # .c
    roomShapeData.source = "\n".join(
        (
            roomShapeName + " = {",
            indent + f"{mesh.roomShape},",
            indent + f"{roomShapeArrayCount},",
            indent + f"{roomShapeEntryName},",
            indent + f"{roomShapeEntryName} + {roomShapeArrayCount}",
            "};\n\n",
        )
    )

    roomShapeData.append(getRoomShapeEntries(mesh))
    return roomShapeData


def convertRoomModel(outRoom: OOTRoom, textureExportSettings: TextureExportSettings):
    """Returns the room model data"""
    modelData = CData()
    mesh = outRoom.mesh

    if len(mesh.meshEntries) == 0:
        raise PluginError(f"Error: Room '{outRoom.index}' has no mesh children.")

    # .c
    for entry in mesh.meshEntries:
        if entry.DLGroup.opaque is not None:
            modelData.append(entry.DLGroup.opaque.to_c(mesh.model.f3d))
        if entry.DLGroup.transparent is not None:
            modelData.append(entry.DLGroup.transparent.to_c(mesh.model.f3d))

    modelData.append(mesh.model.to_c(textureExportSettings, OOTGfxFormatter(ScrollMethod.Vertex)).all())
    return modelData
