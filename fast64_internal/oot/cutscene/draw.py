from bpy.types import UILayout, Object
from ...utility import PluginError, prop_split
from ..oot_utility import OOTCollectionAdd, drawCollectionOps
from .operators import OOTCSListAdd, OOTCSTextboxAdd
from .classes import OOTCSListProperty, OOTCutsceneProperty

from ..oot_constants import (
    ootEnumCSTextboxType,
    ootEnumCSListType,
    ootEnumCSTextboxTypeIcons,
    ootEnumCSListTypeIcons,
)


def drawCSListProperty(
    csLayout: UILayout, listProp: OOTCSListProperty, listIndex: int, objName: str, collectionType: str
):
    typeToAttr = {
        "Textbox": "textbox",
        "Lighting": "lighting",
        "Time": "time",
        "PlayBGM": "bgm",
        "StopBGM": "bgm",
        "FadeBGM": "bgm",
        "Misc": "misc",
        "0x09": "nine",
        "Unk": "unk",
    }

    typeToName = {
        "0x09": "Rumble",
    }

    listName = f"'{typeToName.get(listProp.listType, listProp.listType)}' Command List"
    csBox = csLayout.box().column()
    csBox.prop(
        listProp,
        "expandTab",
        text=listName if listProp.listType != "FX" else "Scene Trans FX",
        icon="TRIA_DOWN" if listProp.expandTab else "TRIA_RIGHT",
    )

    if listProp.expandTab:
        attrName = typeToAttr.get(listProp.listType)

        drawCollectionOps(csBox, listIndex, collectionType, None, objName, False)

        if listProp.listType == "FX":
            prop_split(csBox, listProp, "fxType", "Transition")
            prop_split(csBox, listProp, "fxStartFrame", "Start Frame")
            prop_split(csBox, listProp, "fxEndFrame", "End Frame")

        elif listProp.listType == "Unk":
            prop_split(csBox, listProp, "unkType", "Unk List Type")

        if attrName is not None:
            csProp = getattr(listProp, attrName)

            if listProp.listType == "Textbox":
                row = csBox.row(align=True)
                for i in range(3):
                    addOp: OOTCollectionAdd = row.operator(
                        OOTCSTextboxAdd.bl_idname,
                        text=f"Add {ootEnumCSTextboxType[i][1]}",
                        icon=ootEnumCSTextboxTypeIcons[i],
                    )

                    addOp.collectionType = collectionType + ".textbox"
                    addOp.textboxType = ootEnumCSTextboxType[i][0]
                    addOp.listIndex = listIndex
                    addOp.objName = objName
            else:
                addOp: OOTCollectionAdd = csBox.operator(
                    OOTCollectionAdd.bl_idname, text="Add item to " + listProp.listType + " List"
                )
                addOp.option = len(csProp)
                addOp.collectionType = collectionType + "." + attrName
                addOp.subIndex = listIndex
                addOp.objName = objName

            for i, curProp in enumerate(csProp):
                curProp.draw(csBox, listProp, listIndex, i, objName, collectionType)

            if len(csProp) == 0:
                csBox.label(text="No items in " + listProp.listType + " List.")


def drawCSAddButtons(layout: UILayout, objName: str, collectionType: str):
    def addButton(row: UILayout):
        nonlocal i
        op = row.operator(OOTCSListAdd.bl_idname, text=ootEnumCSListType[i][1], icon=ootEnumCSListTypeIcons[i])
        op.collectionType = collectionType
        op.listType = ootEnumCSListType[i][0]
        op.objName = objName
        i += 1

    box = layout.box().column(align=True)
    box.label(text="Add Cutscene Command")

    i = 0
    row = box.row(align=True)
    addButton(row)

    for _ in range(3):
        row = box.row(align=True)
        for _ in range(3):
            addButton(row)

    box.label(text="Install zcamedit for camera/actor motion.")


def drawCutsceneProperty(csLayout: UILayout, obj: Object):
    csProp: OOTCutsceneProperty = obj.ootCutsceneProperty

    csLayout.prop(csProp, "csEndFrame")

    csLayout.prop(csProp, "csWriteTerminator")
    if csProp.csWriteTerminator:
        destRow = csLayout.row()
        destRow.prop(csProp, "csTermIdx")
        destRow.prop(csProp, "csTermStart")
        destRow.prop(csProp, "csTermEnd")

    drawCSAddButtons(csLayout, obj.name, "Cutscene")

    for i, listProp in enumerate(csProp.csLists):
        drawCSListProperty(csLayout, listProp, i, obj.name, "Cutscene")
