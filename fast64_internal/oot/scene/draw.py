from bpy.types import UILayout
from ...utility import prop_split
from ..oot_utility import drawAddButton, drawCollectionOps, drawEnumWithCustom
from ..oot_cutscene import drawCSListProperty, drawCSAddButtons
from .operators import OOT_SearchMusicSeqEnumOperator
from .classes import (
    OOTExitProperty,
    OOTLightProperty,
    OOTLightGroupProperty,
    OOTSceneTableEntryProperty,
    OOTSceneHeaderProperty,
    OOTAlternateSceneHeaderProperty,
)


def drawExitProperty(layout: UILayout, exitProp: OOTExitProperty, index: int, headerIndex: int, objName: str):
    box = layout.box()
    box.prop(
        exitProp, "expandTab", text="Exit " + str(index + 1), icon="TRIA_DOWN" if exitProp.expandTab else "TRIA_RIGHT"
    )

    if exitProp.expandTab:
        drawCollectionOps(box, index, "Exit", headerIndex, objName)
        drawEnumWithCustom(box, exitProp, "exitIndex", "Exit Index", "")
        if exitProp.exitIndex != "Custom":
            box.label(text='This is unfinished, use "Custom".')
            exitGroup = box.column()
            exitGroup.enabled = False
            drawEnumWithCustom(exitGroup, exitProp, "scene", "Scene", "")
            exitGroup.prop(exitProp, "continueBGM", text="Continue BGM")
            exitGroup.prop(exitProp, "displayTitleCard", text="Display Title Card")
            drawEnumWithCustom(exitGroup, exitProp, "fadeInAnim", "Fade In Animation", "")
            drawEnumWithCustom(exitGroup, exitProp, "fadeOutAnim", "Fade Out Animation", "")


def drawLightProperty(
    layout: UILayout,
    lightProp: OOTLightProperty,
    name: str,
    showExpandTab: bool,
    index: int,
    sceneHeaderIndex: int,
    objName: str,
):
    if showExpandTab:
        box = layout.box().column()
        box.prop(lightProp, "expandTab", text=name, icon="TRIA_DOWN" if lightProp.expandTab else "TRIA_RIGHT")
        expandTab = lightProp.expandTab
    else:
        box = layout
        expandTab = True

    if expandTab:
        if index is not None:
            drawCollectionOps(box, index, "Light", sceneHeaderIndex, objName)
        prop_split(box, lightProp, "ambient", "Ambient Color")

        if lightProp.useCustomDiffuse0:
            prop_split(box, lightProp, "diffuse0Custom", "Diffuse 0")
            box.label(text="Make sure light is not part of scene hierarchy.", icon="FILE_PARENT")
        else:
            prop_split(box, lightProp, "diffuse0", "Diffuse 0")
        box.prop(lightProp, "useCustomDiffuse0")

        if lightProp.useCustomDiffuse1:
            prop_split(box, lightProp, "diffuse1Custom", "Diffuse 1")
            box.label(text="Make sure light is not part of scene hierarchy.", icon="FILE_PARENT")
        else:
            prop_split(box, lightProp, "diffuse1", "Diffuse 1")
        box.prop(lightProp, "useCustomDiffuse1")

        prop_split(box, lightProp, "fogColor", "Fog Color")
        prop_split(box, lightProp, "fogNear", "Fog Near")
        prop_split(box, lightProp, "fogFar", "Fog Far")
        prop_split(box, lightProp, "transitionSpeed", "Transition Speed")


def drawLightGroupProperty(layout: UILayout, lightGroupProp: OOTLightGroupProperty):
    box = layout.column()
    box.row().prop(lightGroupProp, "menuTab", expand=True)
    todNames = [("Dawn", "dawn"), ("Day", "day"), ("Dusk", "dusk"), ("Night", "night")]

    for tabName, prop in todNames:
        if lightGroupProp.menuTab == tabName:
            drawLightProperty(box, getattr(lightGroupProp, prop), tabName, False, None, None, None)


def drawSceneTableEntryProperty(layout: UILayout, sceneTableEntryProp: OOTSceneTableEntryProperty):
    prop_split(layout, sceneTableEntryProp, "drawConfig", "Draw Config")


def drawSceneHeaderProperty(
    layout: UILayout, sceneProp: OOTSceneHeaderProperty, dropdownLabel: str, headerIndex: int, objName: str
):
    if dropdownLabel is not None:
        layout.prop(
            sceneProp, "expandTab", text=dropdownLabel, icon="TRIA_DOWN" if sceneProp.expandTab else "TRIA_RIGHT"
        )
        if not sceneProp.expandTab:
            return

    if headerIndex is not None and headerIndex > 3:
        drawCollectionOps(layout, headerIndex - 4, "Scene", None, objName)

    if headerIndex is not None and headerIndex > 0 and headerIndex < 4:
        layout.prop(sceneProp, "usePreviousHeader", text="Use Previous Header")
        if sceneProp.usePreviousHeader:
            return

    if headerIndex is None or headerIndex == 0:
        layout.row().prop(sceneProp, "menuTab", expand=True)
        menuTab = sceneProp.menuTab
    else:
        layout.row().prop(sceneProp, "altMenuTab", expand=True)
        menuTab = sceneProp.altMenuTab

    if menuTab == "General":
        general = layout.column()
        general.box().label(text="General")

        if headerIndex is None or headerIndex == 0:
            drawSceneTableEntryProperty(layout, sceneProp.sceneTableEntry)

        drawEnumWithCustom(general, sceneProp, "globalObject", "Global Object", "")
        drawEnumWithCustom(general, sceneProp, "naviCup", "Navi Hints", "")

        skyboxAndSound = layout.column()
        skyboxAndSound.box().label(text="Skybox And Sound")
        drawEnumWithCustom(skyboxAndSound, sceneProp, "skyboxID", "Skybox", "")
        drawEnumWithCustom(skyboxAndSound, sceneProp, "skyboxCloudiness", "Cloudiness", "")
        drawEnumWithCustom(skyboxAndSound, sceneProp, "musicSeq", "Music Sequence", "")

        musicSearch = skyboxAndSound.operator(OOT_SearchMusicSeqEnumOperator.bl_idname, icon="VIEWZOOM")
        musicSearch.objName = objName
        musicSearch.headerIndex = headerIndex if headerIndex is not None else 0
        drawEnumWithCustom(skyboxAndSound, sceneProp, "nightSeq", "Nighttime SFX", "")
        drawEnumWithCustom(skyboxAndSound, sceneProp, "audioSessionPreset", "Audio Session Preset", "")

        cameraAndWorldMap = layout.column()
        cameraAndWorldMap.box().label(text="Camera And World Map")
        drawEnumWithCustom(cameraAndWorldMap, sceneProp, "mapLocation", "Map Location", "")
        drawEnumWithCustom(cameraAndWorldMap, sceneProp, "cameraMode", "Camera Mode", "")

    elif menuTab == "Lighting":
        lighting = layout.column()
        lighting.box().label(text="Lighting List")
        drawEnumWithCustom(lighting, sceneProp, "skyboxLighting", "Lighting Mode", "")

        if sceneProp.skyboxLighting == "0x00":  # Time of Day
            drawLightGroupProperty(lighting, sceneProp.timeOfDayLights)
        else:
            for i in range(len(sceneProp.lightList)):
                drawLightProperty(lighting, sceneProp.lightList[i], "Lighting " + str(i), True, i, headerIndex, objName)
            drawAddButton(lighting, len(sceneProp.lightList), "Light", headerIndex, objName)

    elif menuTab == "Cutscene":
        cutscene = layout.column()
        r = cutscene.row()
        r.prop(sceneProp, "writeCutscene", text="Write Cutscene")
        if sceneProp.writeCutscene:
            r.prop(sceneProp, "csWriteType", text="Data")

            if sceneProp.csWriteType == "Custom":
                cutscene.prop(sceneProp, "csWriteCustom")
            elif sceneProp.csWriteType == "Object":
                cutscene.prop(sceneProp, "csWriteObject")
            else:
                # This is the GUI setup / drawing for the properties for the
                # deprecated "Embedded" cutscene type. They have not been removed
                # as doing so would break any existing scenes made with this type
                # of cutscene data.
                cutscene.label(text='Embedded cutscenes are deprecated. Please use "Object" instead.')
                cutscene.prop(sceneProp, "csEndFrame", text="End Frame")
                cutscene.prop(sceneProp, "csWriteTerminator", text="Write Terminator (Code Execution)")
                if sceneProp.csWriteTerminator:
                    r = cutscene.row()
                    r.prop(sceneProp, "csTermIdx", text="Index")
                    r.prop(sceneProp, "csTermStart", text="Start Frm")
                    r.prop(sceneProp, "csTermEnd", text="End Frm")
                collectionType = "CSHdr." + str(0 if headerIndex is None else headerIndex)
                for i, p in enumerate(sceneProp.csLists):
                    drawCSListProperty(cutscene, p, i, objName, collectionType)
                drawCSAddButtons(cutscene, objName, collectionType)
        if headerIndex is None or headerIndex == 0:
            cutscene.label(text="Extra cutscenes (not in any header):")
            for i in range(len(sceneProp.extraCutscenes)):
                box = cutscene.box().column()
                drawCollectionOps(box, i, "extraCutscenes", None, objName, True)
                box.prop(sceneProp.extraCutscenes[i], "csObject", text="CS obj")
            if len(sceneProp.extraCutscenes) == 0:
                drawAddButton(cutscene, 0, "extraCutscenes", 0, objName)

    elif menuTab == "Exits":
        if headerIndex is None or headerIndex == 0:
            exitBox = layout.column()
            exitBox.box().label(text="Exit List")
            for i in range(len(sceneProp.exitList)):
                drawExitProperty(exitBox, sceneProp.exitList[i], i, headerIndex, objName)

            drawAddButton(exitBox, len(sceneProp.exitList), "Exit", headerIndex, objName)
        else:
            layout.label(text="Exits are edited in main header.")


def drawAlternateSceneHeaderProperty(layout: UILayout, headerProp: OOTAlternateSceneHeaderProperty, objName: str):
    headerSetup = layout.column()
    altLayers = [
        ("Child Night", "childNightHeader"),
        ("Adult Day", "adultDayHeader"),
        ("Adult Night", "adultNightHeader"),
    ]

    for i, tabName, prop in enumerate(altLayers, 1):
        if headerProp.headerMenuTab == tabName:
            drawSceneHeaderProperty(headerSetup, getattr(headerProp, prop), None, i, objName)

    if headerProp.headerMenuTab == "Cutscene":
        prop_split(headerSetup, headerProp, "currentCutsceneIndex", "Cutscene Index")
        drawAddButton(headerSetup, len(headerProp.cutsceneHeaders), "Scene", None, objName)
        index = headerProp.currentCutsceneIndex

        if index - 4 < len(headerProp.cutsceneHeaders):
            drawSceneHeaderProperty(headerSetup, headerProp.cutsceneHeaders[index - 4], None, index, objName)
        else:
            headerSetup.label(text="No cutscene header for this index.", icon="QUESTION")
