from bpy.types import UILayout
from ...utility import prop_split
from ..utility import drawAddButton, drawCollectionOps, drawEnumWithCustom, getEnumName
from .data import ootEnumObjectID
from .operators import OOT_SearchObjectEnumOperator
from .classes import OOTObjectProperty, OOTRoomHeaderProperty, OOTAlternateRoomHeaderProperty


def drawObjectProperty(layout: UILayout, objectProp: OOTObjectProperty, headerIndex: int, index: int, objName: str):
    objItemBox = layout.box()
    objectName = getEnumName(ootEnumObjectID, objectProp.objectID)
    objItemBox.prop(
        objectProp, "expandTab", text=objectName, icon="TRIA_DOWN" if objectProp.expandTab else "TRIA_RIGHT"
    )
    if objectProp.expandTab:
        drawCollectionOps(objItemBox, index, "Object", headerIndex, objName)
        objSearch = objItemBox.operator(OOT_SearchObjectEnumOperator.bl_idname, icon="VIEWZOOM")
        objSearch.objName = objName
        objItemBox.column().label(text="ID: " + objectName)

        if objectProp.objectID == "Custom":
            prop_split(objItemBox, objectProp, "objectIDCustom", "Object ID Custom")

        objSearch.headerIndex = headerIndex if headerIndex is not None else 0
        objSearch.index = index


def drawRoomHeaderProperty(
    layout: UILayout, roomProp: OOTRoomHeaderProperty, dropdownLabel: str, headerIndex: int, objName: str
):
    if dropdownLabel is not None:
        layout.prop(roomProp, "expandTab", text=dropdownLabel, icon="TRIA_DOWN" if roomProp.expandTab else "TRIA_RIGHT")
        if not roomProp.expandTab:
            return

    if headerIndex is not None and headerIndex > 3:
        drawCollectionOps(layout, headerIndex - 4, "Room", None, objName)

    if headerIndex is not None and headerIndex > 0 and headerIndex < 4:
        layout.prop(roomProp, "usePreviousHeader", text="Use Previous Header")
        if roomProp.usePreviousHeader:
            return

    if headerIndex is None or headerIndex == 0:
        layout.row().prop(roomProp, "menuTab", expand=True)
        menuTab = roomProp.menuTab
    else:
        layout.row().prop(roomProp, "altMenuTab", expand=True)
        menuTab = roomProp.altMenuTab

    if menuTab == "General":
        if headerIndex is None or headerIndex == 0:
            general = layout.column()
            general.box().label(text="General")
            prop_split(general, roomProp, "roomIndex", "Room Index")
            prop_split(general, roomProp, "roomShape", "Mesh Type")
            if roomProp.roomShape == "ROOM_SHAPE_TYPE_IMAGE":
                general.box().label(text="Image Room Shape not supported at this time.")
            if roomProp.roomShape == "ROOM_SHAPE_TYPE_CULLABLE":
                prop_split(general, roomProp, "defaultCullDistance", "Default Cull (Blender Units)")

        # Behaviour
        behaviourBox = layout.column()
        behaviourBox.box().label(text="Behaviour")
        drawEnumWithCustom(behaviourBox, roomProp, "roomBehaviour", "Room Behaviour", "")

        behaviourBox.prop(roomProp, "roomIsHot")
        if not roomProp.roomIsHot:
            drawEnumWithCustom(behaviourBox, roomProp, "linkIdleMode", "Link Idle Mode", "")

        behaviourBox.prop(roomProp, "disableWarpSongs", text="Disable Warp Songs")
        behaviourBox.prop(roomProp, "showInvisibleActors", text="Show Invisible Actors")

        # Time
        skyboxAndTime = layout.column()
        skyboxAndTime.box().label(text="Skybox And Time")

        # Skybox
        skyboxAndTime.prop(roomProp, "disableSkybox", text="Disable Skybox")
        skyboxAndTime.prop(roomProp, "disableSunMoon", text="Disable Sun/Moon")
        skyboxAndTime.prop(roomProp, "leaveTimeUnchanged", text="Leave Time Unchanged")

        if not roomProp.leaveTimeUnchanged:
            skyboxAndTime.label(text="Time")
            timeRow = skyboxAndTime.row()
            timeRow.prop(roomProp, "timeHours", text="Hours")
            timeRow.prop(roomProp, "timeMinutes", text="Minutes")

        prop_split(skyboxAndTime, roomProp, "timeSpeed", "Time Speed")

        # Echo
        prop_split(skyboxAndTime, roomProp, "echo", "Echo")

        # Wind
        windBox = layout.column()
        windBox.box().label(text="Wind")
        windBox.prop(roomProp, "setWind", text="Set Wind")
        if roomProp.setWind:
            windBox.label(text="Wind Direction (X, Y, Z)")
            windBox.row().prop(roomProp, "windVector", text="")

    elif menuTab == "Objects":
        objBox = layout.column()
        objBox.box().label(text="Objects")
        for i in range(len(roomProp.objectList)):
            drawObjectProperty(objBox, roomProp.objectList[i], headerIndex, i, objName)
        drawAddButton(objBox, len(roomProp.objectList), "Object", headerIndex, objName)


def drawAlternateRoomHeaderProperty(layout: UILayout, headerProp: OOTAlternateRoomHeaderProperty, objName: str):
    headerSetup = layout.column()
    altLayers = [
        ("Child Night", "childNightHeader"),
        ("Adult Day", "adultDayHeader"),
        ("Adult Night", "adultNightHeader"),
    ]

    headerSetup.row().prop(headerProp, "headerMenuTab", expand=True)
    for i, (tabName, prop) in enumerate(altLayers, 1):
        if headerProp.headerMenuTab == tabName:
            drawRoomHeaderProperty(headerSetup, getattr(headerProp, prop), None, i, objName)

    if headerProp.headerMenuTab == "Cutscene":
        prop_split(headerSetup, headerProp, "currentCutsceneIndex", "Cutscene Index")
        drawAddButton(headerSetup, len(headerProp.cutsceneHeaders), "Room", None, objName)
        index = headerProp.currentCutsceneIndex

        if index - 4 < len(headerProp.cutsceneHeaders):
            drawRoomHeaderProperty(headerSetup, headerProp.cutsceneHeaders[index - 4], None, index, objName)
        else:
            headerSetup.label(text="No cutscene header for this index.", icon="QUESTION")
