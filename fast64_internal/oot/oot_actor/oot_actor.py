from bpy.types import UILayout
from ...utility import prop_split, label_split
from ..oot_utility import drawAddButton, drawCollectionOps, getEnumName, drawEnumWithCustom
from ..oot_constants import ootEnumActorID
from ..oot_scene_room import OOTAlternateRoomHeaderProperty, OOTAlternateSceneHeaderProperty
from .oot_actor_operators import OOT_SearchActorIDEnumOperator
from .oot_actor_classes import (
    OOTActorHeaderItemProperty,
    OOTActorHeaderProperty,
    OOTActorProperty,
    OOTTransitionActorProperty,
    OOTEntranceProperty,
)


def drawActorHeaderProperty(
    layout: UILayout,
    headerProp: OOTActorHeaderProperty,
    propUser: str,
    altProp: OOTAlternateRoomHeaderProperty,
    objName: str,
):
    headerSetup = layout.column()
    prop_split(headerSetup, headerProp, "sceneSetupPreset", "Scene Layer Preset")

    if headerProp.sceneSetupPreset == "Custom":
        headerSetupBox = headerSetup.column()
        headerSetupBox.prop(headerProp, "childDayHeader", text="Child Day")
        prevHeaderName = "childDayHeader"
        childNightRow = headerSetupBox.row()

        if altProp is None or altProp.childNightHeader.usePreviousHeader:
            # Draw previous header checkbox (so get previous state), but labeled
            # as current one and grayed out
            childNightRow.prop(headerProp, prevHeaderName, text="Child Night")
            childNightRow.enabled = False
        else:
            childNightRow.prop(headerProp, "childNightHeader", text="Child Night")
            prevHeaderName = "childNightHeader"

        adultDayRow = headerSetupBox.row()
        if altProp is None or altProp.adultDayHeader.usePreviousHeader:
            adultDayRow.prop(headerProp, prevHeaderName, text="Adult Day")
            adultDayRow.enabled = False
        else:
            adultDayRow.prop(headerProp, "adultDayHeader", text="Adult Day")
            prevHeaderName = "adultDayHeader"

        adultNightRow = headerSetupBox.row()
        if altProp is None or altProp.adultNightHeader.usePreviousHeader:
            adultNightRow.prop(headerProp, prevHeaderName, text="Adult Night")
            adultNightRow.enabled = False
        else:
            adultNightRow.prop(headerProp, "adultNightHeader", text="Adult Night")

        headerSetupBox.row().label(text="Cutscene headers to include this actor in:")
        for i, csLayer in enumerate(headerProp.cutsceneHeaders):
            drawActorHeaderItemProperty(headerSetup, propUser, csLayer, i, altProp, objName)

        drawAddButton(headerSetup, len(headerProp.cutsceneHeaders), propUser, None, objName)


def drawActorHeaderItemProperty(
    layout: UILayout,
    propUser: str,
    headerItemProp: OOTActorHeaderItemProperty,
    index: int,
    altProp: OOTAlternateRoomHeaderProperty,
    objName: str,
):
    box = layout.box()
    box.prop(
        headerItemProp,
        "expandTab",
        text=f"Header {headerItemProp.headerIndex}",
        icon="TRIA_DOWN" if headerItemProp.expandTab else "TRIA_RIGHT",
    )

    if headerItemProp.expandTab:
        drawCollectionOps(box, index, propUser, None, objName)
        prop_split(box, headerItemProp, "headerIndex", "Header Index")
        if altProp is not None and headerItemProp.headerIndex >= len(altProp.cutsceneHeaders) + 4:
            box.label(text="Header does not exist.", icon="QUESTION")


def drawActorProperty(
    layout: UILayout, actorProp: OOTActorProperty, altRoomProp: OOTAlternateRoomHeaderProperty, objName: str
):
    actorIDBox = layout.column()
    searchOp = actorIDBox.operator(OOT_SearchActorIDEnumOperator.bl_idname, icon="VIEWZOOM")
    searchOp.actorUser = "Actor"
    searchOp.objName = objName

    split = actorIDBox.split(factor=0.5)
    split.label(text="Actor ID")
    split.label(text=getEnumName(ootEnumActorID, actorProp.actorID))

    if actorProp.actorID == "Custom":
        prop_split(actorIDBox, actorProp, "actorIDCustom", "")

    prop_split(actorIDBox, actorProp, "actorParam", "Actor Parameter")

    actorIDBox.prop(actorProp, "rotOverride", text="Override Rotation (ignore Blender rot)")
    if actorProp.rotOverride:
        prop_split(actorIDBox, actorProp, "rotOverrideX", "Rot X")
        prop_split(actorIDBox, actorProp, "rotOverrideY", "Rot Y")
        prop_split(actorIDBox, actorProp, "rotOverrideZ", "Rot Z")

    drawActorHeaderProperty(actorIDBox, actorProp.headerSettings, "Actor", altRoomProp, objName)


def drawTransitionActorProperty(
    layout: UILayout,
    transActorProp: OOTTransitionActorProperty,
    altSceneProp: OOTAlternateSceneHeaderProperty,
    roomIndex: int,
    objName: str,
):
    transActor: OOTActorProperty = transActorProp.actor
    transLayout = layout.column()
    searchOp = transLayout.operator(OOT_SearchActorIDEnumOperator.bl_idname, icon="VIEWZOOM")
    searchOp.actorUser = "Transition Actor"
    searchOp.objName = objName

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

    drawActorHeaderProperty(transLayout, transActor.headerSettings, "Transition Actor", altSceneProp, objName)


def drawEntranceProperty(
    entranceLayout: UILayout,
    entranceProp: OOTEntranceProperty,
    altSceneProp: OOTAlternateSceneHeaderProperty,
    objName: str,
):
    prop_split(entranceLayout, entranceProp, "spawnIndex", "Spawn Index")
    prop_split(entranceLayout, entranceProp.actor, "actorParam", "Actor Param")

    entranceLayout.prop(entranceProp, "customActor")
    if entranceProp.customActor:
        prop_split(entranceLayout, entranceProp.actor, "actorIDCustom", "Actor ID Custom")

    drawActorHeaderProperty(entranceLayout, entranceProp.actor.headerSettings, "Entrance", altSceneProp, objName)
