from bpy.types import UILayout
from ......utility import prop_split, label_split
from .....utility import drawAddButton, drawCollectionOps, getEnumName, drawEnumWithCustom
from ..room import OOTAlternateRoomHeaderProperty
from .operators import OOT_SearchActorIDEnumOperator
from .data import ootEnumActorID

from .classes import (
    OOTActorHeaderItemProperty,
    OOTActorHeaderProperty,
    OOTActorProperty,
    OOTTransitionActorProperty,
    OOTEntranceProperty,
)


def drawActorCutsceneLayerItem(
    layout: UILayout,
    propUser: str,
    csLayerItemProp: OOTActorHeaderItemProperty,
    index: int,
    altProp: OOTAlternateRoomHeaderProperty,
    objName: str,
):
    """Draws a single cutscene layer index to include an actor"""
    box = layout.box()
    box.prop(
        csLayerItemProp,
        "expandTab",
        text=f"Cutscene Layer n°{csLayerItemProp.headerIndex - 3}",
        icon="TRIA_DOWN" if csLayerItemProp.expandTab else "TRIA_RIGHT",
    )

    if csLayerItemProp.expandTab:
        drawCollectionOps(box, index, propUser, None, objName)
        prop_split(box, csLayerItemProp, "headerIndex", "Cutscene Layer Index")
        if altProp is not None and csLayerItemProp.headerIndex >= len(altProp.cutsceneHeaders) + 4:
            box.label(text="Header does not exist.", icon="QUESTION")


def drawActorHeaderProperty(
    layout: UILayout,
    headerProp: OOTActorHeaderProperty,
    propUser: str,
    altProp: OOTAlternateRoomHeaderProperty,
    objName: str,
):
    """Draws the room layers to include the actor"""
    headerSetup = layout.column()
    prop_split(headerSetup, headerProp, "sceneSetupPreset", "Scene Layer Preset")

    if headerProp.sceneSetupPreset == "Custom":
        headerSetupBox = headerSetup.column()
        headerBoolProps: list[tuple[str, str]] = [
            ("childNightHeader", "Child Night"),
            ("adultDayHeader", "Adult Day"),
            ("adultNightHeader", "Adult Night"),
        ]

        prevProp = "childDayHeader"
        headerSetupBox.prop(headerProp, prevProp, text="Child Day")
        for headerName, headerDesc in headerBoolProps:
            headerRow = headerSetupBox.row()
            if altProp is None or getattr(altProp, headerName).usePreviousHeader:
                headerRow.prop(headerProp, prevProp, text=headerDesc)
                headerRow.enabled = False
            else:
                prevProp = headerName
                headerRow.prop(headerProp, headerName, text=headerDesc)

        headerSetupBox.row().label(text="Cutscene headers to include this actor in:")
        for i, csLayer in enumerate(headerProp.cutsceneHeaders):
            drawActorCutsceneLayerItem(headerSetup, propUser, csLayer, i, altProp, objName)

        drawAddButton(headerSetup, len(headerProp.cutsceneHeaders), propUser, None, objName)


def drawActorProperty(layout: UILayout, actorProp: OOTActorProperty, objName: str):
    """Draws the actor's parameters and ID search operator"""
    actorLayout = layout.column()
    idOperator = actorLayout.operator(OOT_SearchActorIDEnumOperator.bl_idname, icon="VIEWZOOM")
    idOperator.actorUser = "Actor"
    idOperator.objName = objName

    split = actorLayout.split(factor=0.5)
    split.label(text="Actor ID")
    split.label(text=getEnumName(ootEnumActorID, actorProp.actorID))

    if actorProp.actorID == "Custom":
        prop_split(actorLayout, actorProp, "actorIDCustom", "")

    prop_split(actorLayout, actorProp, "actorParam", "Actor Parameter")

    actorLayout.prop(actorProp, "rotOverride", text="Override Rotation (ignore Blender rot)")
    if actorProp.rotOverride:
        for rot in ["X", "Y", "Z"]:
            prop_split(actorLayout, actorProp, f"rotOverride{rot}", f"Rot {rot}")


def drawTransitionActorProperty(
    transLayout: UILayout,
    transActorProp: OOTTransitionActorProperty,
    roomIndex: int,
    objName: str,
):
    """Draws the transition actor's parameters and ID search operator"""
    transActor: OOTActorProperty = transActorProp.actor
    idOperator = transLayout.operator(OOT_SearchActorIDEnumOperator.bl_idname, icon="VIEWZOOM")
    idOperator.actorUser = "Transition Actor"
    idOperator.objName = objName

    split = transLayout.split(factor=0.5)
    split.label(text="Actor ID")
    split.label(text=getEnumName(ootEnumActorID, transActor.actorID))

    if transActor.actorID == "Custom":
        prop_split(transLayout, transActor, "actorIDCustom", "")

    prop_split(transLayout, transActor, "actorParam", "Actor Parameter")
    label_split(transLayout, "Room To Transition From", f"{roomIndex}")
    prop_split(transLayout, transActorProp, "roomIndex", "Room To Transition To")
    transLayout.label(text='Y+ side of door faces toward the "from" room.', icon="ORIENTATION_NORMAL")

    for camType in ["Front", "Back"]:
        drawEnumWithCustom(
            transLayout, transActorProp, f"cameraTransition{camType}", f"Camera Transition {camType}", ""
        )


def drawEntranceProperty(entranceLayout: UILayout, entranceProp: OOTEntranceProperty):
    """Draws the entrance actor's parameters and custom ID textbox"""
    prop_split(entranceLayout, entranceProp, "spawnIndex", "Spawn Index")
    prop_split(entranceLayout, entranceProp.actor, "actorParam", "Actor Param")

    entranceLayout.prop(entranceProp, "customActor")
    if entranceProp.customActor:
        prop_split(entranceLayout, entranceProp.actor, "actorIDCustom", "Actor ID Custom")
