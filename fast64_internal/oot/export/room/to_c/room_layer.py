from .....utility import CData
from ....oot_utility import indent
from ...classes.room import OOTRoom
from .commands import ootRoomCommandsToC
from .object import ootObjectListToC
from .actor import ootActorListToC


def ootGetRoomLayerData(room: OOTRoom, headerIndex: int):
    """Returns a room layer's data"""
    layerData = CData()

    if len(room.objectIDList) > 0:
        layerData.append(ootObjectListToC(room, headerIndex))

    if len(room.actorList) > 0:
        layerData.append(ootActorListToC(None, room, headerIndex))

    return layerData


def ootGetRoomAltHeaderEntries(roomLayers: list[OOTRoom]):
    """Returns the layers headers array names"""
    return "\n".join(
        [
            f"{indent + roomLayers[i].getRoomName()}_header{i:02},"
            if roomLayers[i] is not None
            else indent + "NULL,"
            if i < 4
            else ""
            for i in range(1, len(roomLayers))
        ]
    )


def ootRoomLayersToC(room: OOTRoom):
    """Returns the rooms file data"""
    layerInfo = CData()  # array of pointers to invidual layers
    layerData = CData()  # the data of each layer
    roomLayers = [room, room.childNightHeader, room.adultDayHeader, room.adultNightHeader]
    roomLayers.extend(room.cutsceneHeaders)

    if room.hasAltLayers():
        altLayerName = f"SCmdBase* {room.getAltLayersListName()}[]"
        altLayerArray = altLayerName + " = {\n" + ootGetRoomAltHeaderEntries(roomLayers) + "\n};\n\n"

        # .h
        layerInfo.header = f"extern {altLayerName};\n"

    # .c
    for i, layer in enumerate(roomLayers):
        if layer is not None:
            layerData.append(ootRoomCommandsToC(layer, i))
            if i == 0 and room.hasAltLayers():
                layerData.source += altLayerArray
            layerData.append(ootGetRoomLayerData(layer, i))

    roomLayerData = layerInfo
    roomLayerData.append(layerData)
    return roomLayerData
