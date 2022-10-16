import bpy
from bpy.types import UILayout, Object, Bone
from ..utility import PluginError, prop_split, ootGetSceneOrRoomHeader


def drawCollectionOps(layout: UILayout, index: int, collectionType: str, subIndex: int, objName: str, allowAdd=True):
    from .classes import OOTCollectionAdd, OOTCollectionRemove, OOTCollectionMove  # circular import fix

    if subIndex is None:
        subIndex = 0

    buttons = layout.row(align=True)

    if allowAdd:
        addOp: OOTCollectionAdd = buttons.operator(OOTCollectionAdd.bl_idname, text="Add", icon="ADD")
        addOp.option = index + 1
        addOp.collectionType = collectionType
        addOp.subIndex = subIndex
        addOp.objName = objName

    removeOp: OOTCollectionRemove = buttons.operator(OOTCollectionRemove.bl_idname, text="Delete", icon="REMOVE")
    removeOp.option = index
    removeOp.collectionType = collectionType
    removeOp.subIndex = subIndex
    removeOp.objName = objName

    moveUp: OOTCollectionMove = buttons.operator(OOTCollectionMove.bl_idname, text="Up", icon="TRIA_UP")
    moveUp.option = index
    moveUp.offset = -1
    moveUp.collectionType = collectionType
    moveUp.subIndex = subIndex
    moveUp.objName = objName

    moveDown: OOTCollectionMove = buttons.operator(OOTCollectionMove.bl_idname, text="Down", icon="TRIA_DOWN")
    moveDown.option = index
    moveDown.offset = 1
    moveDown.collectionType = collectionType
    moveDown.subIndex = subIndex
    moveDown.objName = objName


def drawAddButton(layout: UILayout, index: int, collectionType: str, subIndex: int, objName: str):
    from .classes import OOTCollectionAdd  # circular import fix

    if subIndex is None:
        subIndex = 0

    addOp: OOTCollectionAdd = layout.operator(OOTCollectionAdd.bl_idname)
    addOp.option = index
    addOp.collectionType = collectionType
    addOp.subIndex = subIndex
    addOp.objName = objName


def getCollectionFromIndex(obj: Object, prop: str, subIndex: int, isRoom: bool):
    header = ootGetSceneOrRoomHeader(obj, subIndex, isRoom)
    return getattr(header, prop)


# Operators cannot store mutable references (?), so to reuse PropertyCollection modification code we do this.
# Save a string identifier in the operator, then choose the member variable based on that.
# subIndex is for a collection within a collection element
def getCollection(objName: str, collectionType: str, subIndex: int):
    obj = bpy.data.objects[objName]

    if collectionType == "Actor":
        collection = obj.ootActorProperty.headerSettings.cutsceneHeaders
    elif collectionType == "Transition Actor":
        collection = obj.ootTransitionActorProperty.actor.headerSettings.cutsceneHeaders
    elif collectionType == "Entrance":
        collection = obj.ootEntranceProperty.actor.headerSettings.cutsceneHeaders
    elif collectionType == "Room":
        collection = obj.ootAlternateRoomHeaders.cutsceneHeaders
    elif collectionType == "Scene":
        collection = obj.ootAlternateSceneHeaders.cutsceneHeaders
    elif collectionType == "Light":
        collection = getCollectionFromIndex(obj, "lightList", subIndex, False)
    elif collectionType == "Exit":
        collection = getCollectionFromIndex(obj, "exitList", subIndex, False)
    elif collectionType == "Object":
        collection = getCollectionFromIndex(obj, "objectList", subIndex, True)
    elif collectionType.startswith("CSHdr."):
        # CSHdr.HeaderNumber[.ListType]
        # Specifying ListType means uses subIndex
        toks = collectionType.split(".")
        assert len(toks) in [2, 3]
        hdrnum = int(toks[1])
        collection = getCollectionFromIndex(obj, "csLists", hdrnum, False)

        if len(toks) == 3:
            collection = getattr(collection[subIndex], toks[2])
    elif collectionType.startswith("Cutscene."):
        # Cutscene.ListType
        toks = collectionType.split(".")
        assert len(toks) == 2
        collection = obj.ootCutsceneProperty.csLists
        collection = getattr(collection[subIndex], toks[1])
    elif collectionType == "Cutscene":
        collection = obj.ootCutsceneProperty.csLists
    elif collectionType == "extraCutscenes":
        collection = obj.ootSceneHeader.extraCutscenes
    else:
        raise PluginError("Invalid collection type: " + collectionType)

    return collection


def getEnumName(enumItems, value):
    for enumTuple in enumItems:
        if enumTuple[0] == value:
            return enumTuple[1]
    raise PluginError(f"Could not find enum value {value}")


def drawEnumWithCustom(panel: UILayout, data, attribute: str, name: str, customName: str):
    prop_split(panel, data, attribute, name)

    if getattr(data, attribute) == "Custom":
        prop_split(panel, data, attribute + "Custom", customName)


def getSortedChildren(bone: Bone):
    return sorted(
        [child.name for child in bone.children if child.ootBoneType != "Ignore"],
        key=lambda childName: childName.lower(),
    )


def getStartBone(armatureObj: Object):
    startBoneNames = [
        bone.name for bone in armatureObj.data.bones if bone.parent is None and bone.ootBoneType != "Ignore"
    ]

    if len(startBoneNames) == 0:
        raise PluginError(f'{armatureObj.name} does not have any root bones that are not of the "Ignore" type.')

    startBoneName = startBoneNames[0]
    return startBoneName
