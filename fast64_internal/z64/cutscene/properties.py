import bpy

from bpy.types import PropertyGroup, Object, UILayout, Scene, Context
from bpy.props import (
    StringProperty,
    EnumProperty,
    IntProperty,
    BoolProperty,
    CollectionProperty,
    PointerProperty,
    FloatVectorProperty,
)
from bpy.utils import register_class, unregister_class
from ...utility import PluginError, prop_split
from ..utility import OOTCollectionAdd, drawCollectionOps, getEnumName, is_oot_features
from ...game_data import game_data
from ..upgrade import upgradeCutsceneSubProps, upgradeCSListProps, upgradeCutsceneProperty
from .operators import OOTCSTextAdd, OOT_SearchCSDestinationEnumOperator, OOTCSListAdd, OOT_SearchCSSeqOperator
from .motion.preview import previewFrameHandler
from .motion.utility import getCutsceneCamera

from .motion.operators import (
    CutsceneCmdPlayPreview,
    CutsceneCmdCreateCameraShot,
    CutsceneCmdCreatePlayerCueList,
    CutsceneCmdCreateActorCueList,
)

from .constants import (
    ootEnumCSTextboxType,
    ootEnumCSTextboxTypeIcons,
    ootCSSubPropToName,
    csListTypeToIcon,
)


class OOTCutsceneCommon:
    attrName = None
    subprops = ["startFrame", "endFrame"]
    expandTab: BoolProperty(default=True)
    startFrame: IntProperty(name="", default=0, min=0)
    endFrame: IntProperty(name="", default=0, min=0)

    def getName(self):
        pass

    def filterProp(self, name, listProp):
        return True

    def filterName(self, name, listProp):
        return name

    def draw_props(
        self,
        layout: UILayout,
        listProp: "OOTCSListProperty",
        listIndex: int,
        cmdIndex: int,
        objName: str,
        collectionType: str,
        tabName: str,
    ):
        # Draws list elements
        box = layout.box().column()

        box.prop(
            self,
            "expandTab",
            text=f"{tabName if tabName != 'Text' else self.getName()} No. {cmdIndex}",
            icon="TRIA_DOWN" if self.expandTab else "TRIA_RIGHT",
        )
        if not self.expandTab:
            return

        drawCollectionOps(box, cmdIndex, collectionType + "." + self.attrName, listIndex, objName)

        for p in self.subprops:
            if game_data.z64.is_oot() and p == "rumble_type" and not bpy.context.scene.fast64.oot.mm_features:
                continue

            if self.filterProp(p, listProp):
                name = self.filterName(p, listProp)
                displayName = ootCSSubPropToName[name]

                if name == "csSeqPlayer":
                    # change the property name to draw the other enum for fade seq command
                    p = name

                prop_split(box, self, p, displayName)

                if name == "csSeqID":
                    seqOp = box.operator(OOT_SearchCSSeqOperator.bl_idname)
                    seqOp.itemIndex = cmdIndex
                    seqOp.listType = listProp.listType

                customValues = [
                    "csMiscType",
                    "csTextType",
                    "ocarinaAction",
                    "csSeqID",
                    "csSeqPlayer",
                    "rumble_type",
                    "transition_type",
                    "blur_type",
                    "trans_general_type",
                    "credits_scene_type",
                    "mod_seq_type",
                ]
                value = getattr(self, p)
                if name in customValues and value == "Custom":
                    prop_split(box, self, f"{name}_custom" if "_" in p else f"{name}Custom", f"{displayName} Custom")

                if name == "csTextType" and value != "choice":
                    break


class OOTCSTextProperty(OOTCutsceneCommon, PropertyGroup):
    attrName = "textList"
    subprops = [
        "textID",
        "ocarinaAction",
        "startFrame",
        "endFrame",
        "csTextType",
        "topOptionTextID",
        "bottomOptionTextID",
        "ocarinaMessageId",
    ]
    textboxType: EnumProperty(items=ootEnumCSTextboxType)

    # subprops
    textID: StringProperty(name="", default="0x0000")
    ocarinaAction: EnumProperty(
        name="Ocarina Action",
        items=lambda self, context: game_data.z64.get_enum("ocarinaAction"),
        default=1,
    )
    ocarinaActionCustom: StringProperty(default="OCARINA_ACTION_CUSTOM")
    topOptionTextID: StringProperty(name="", default="0x0000")
    bottomOptionTextID: StringProperty(name="", default="0x0000")
    ocarinaMessageId: StringProperty(name="", default="0x0000")
    csTextType: EnumProperty(
        name="Text Type", items=lambda self, context: game_data.z64.get_enum("csTextType"), default=1
    )
    csTextTypeCustom: StringProperty(default="CS_TEXT_CUSTOM")

    def getName(self):
        return getEnumName(ootEnumCSTextboxType, self.textboxType)

    def filterProp(self, name, listProp):
        if self.textboxType == "Text":
            return name not in ["ocarinaAction", "ocarinaMessageId"]
        elif self.textboxType == "None":
            return name in ["startFrame", "endFrame"]
        elif self.textboxType == "OcarinaAction":
            return name in ["ocarinaAction", "startFrame", "endFrame", "ocarinaMessageId"]
        else:
            raise PluginError("Invalid property name for OOTCSTextProperty")


class OOTCSLightSettingsProperty(OOTCutsceneCommon, PropertyGroup):
    attrName = "lightSettingsList"
    subprops = ["lightSettingsIndex", "startFrame"]
    lightSettingsIndex: IntProperty(name="", default=0, min=0)


class OOTCSTimeProperty(OOTCutsceneCommon, PropertyGroup):
    attrName = "timeList"
    subprops = ["startFrame", "hour", "minute"]
    hour: IntProperty(name="", default=23, min=0, max=23)
    minute: IntProperty(name="", default=59, min=0, max=59)


class OOTCSSeqProperty(OOTCutsceneCommon, PropertyGroup):
    attrName = "seqList"
    subprops = ["csSeqID", "startFrame", "endFrame"]
    csSeqID: EnumProperty(name="Seq ID", items=lambda self, context: game_data.z64.get_enum("seqId"), default=1)
    csSeqIDCustom: StringProperty(default="NA_BGM_CUSTOM")
    csSeqPlayer: EnumProperty(
        name="Seq Player", items=lambda self, context: game_data.z64.get_enum("csSeqPlayer"), default=1
    )
    csSeqPlayerCustom: StringProperty(default="CS_FADE_OUT_CUSTOM")

    def filterProp(self, name, listProp):
        types = {"FadeOutSeqList", "StopSeqList"} if game_data.z64.is_mm() else {"FadeOutSeqList"}
        return name != "endFrame" or listProp.listType in types

    def filterName(self, name, listProp):
        if name == "csSeqID" and listProp.listType == "FadeOutSeqList":
            return "csSeqPlayer"
        return name


class OOTCSMiscProperty(OOTCutsceneCommon, PropertyGroup):
    attrName = "miscList"
    subprops = ["csMiscType", "startFrame", "endFrame"]
    csMiscType: EnumProperty(name="Type", items=lambda self, context: game_data.z64.get_enum("csMiscType"), default=1)
    csMiscTypeCustom: StringProperty(default="CS_MISC_CUSTOM")


class OOTCSRumbleProperty(OOTCutsceneCommon, PropertyGroup):
    attrName = "rumbleList"
    subprops = ["rumble_type", "startFrame", "rumbleSourceStrength", "rumbleDuration", "rumbleDecreaseRate"]

    # those variables are unsigned chars in decomp
    # see https://github.com/zeldaret/oot/blob/542012efa68d110d6b631f9d149f6e5f4e68cc8e/src/code/z_rumble.c#L58-L77
    rumbleSourceStrength: IntProperty(name="", default=0, min=0, max=255)
    rumbleDuration: IntProperty(name="", default=0, min=0, max=255)
    rumbleDecreaseRate: IntProperty(name="", default=0, min=0, max=255)
    rumble_type: EnumProperty(name="", items=game_data.z64.enums.enum_cs_rumble_type, default=1)
    rumble_type_custom: StringProperty()


class OOTCSTransitionProperty(OOTCutsceneCommon, PropertyGroup):
    attrName = "transition_list"
    subprops = ["transition_type", "startFrame", "endFrame"]

    transition_type: EnumProperty(
        name="", items=lambda self, context: game_data.z64.get_enum("transitionType"), default=1
    )
    transition_type_custom: StringProperty("CS_TRANS_CUSTOM")


class OOTCSMotionBlurProperty(OOTCutsceneCommon, PropertyGroup):
    attrName = "motion_blur_list"
    subprops = ["blur_type", "startFrame", "endFrame"]

    blur_type: EnumProperty(name="", items=lambda self, context: game_data.z64.get_enum("blur_type"), default=1)
    blur_type_custom: StringProperty("CS_TRANS_CUSTOM")


class OOTCSTransitionGeneralProperty(OOTCutsceneCommon, PropertyGroup):
    attrName = "trans_general_list"
    subprops = ["trans_general_type", "startFrame", "endFrame", "trans_color"]

    trans_general_type: EnumProperty(
        name="", items=lambda self, context: game_data.z64.get_enum("trans_general"), default=1
    )
    trans_general_type_custom: StringProperty("CS_TRANS_GENERAL_CUSTOM")

    trans_color: FloatVectorProperty(
        name="Color",
        subtype="COLOR",
        size=4,
        min=0,
        max=1,
        default=(1, 1, 1, 1),
    )


class OOTCSChooseCreditsSceneProperty(OOTCutsceneCommon, PropertyGroup):
    attrName = "credits_scene_list"
    subprops = ["credits_scene_type", "startFrame"]

    credits_scene_type: EnumProperty(
        name="", items=lambda self, context: game_data.z64.get_enum("credits_scene_type"), default=1
    )
    credits_scene_type_custom: StringProperty("CS_CREDITS_CUSTOM")


class OOTCSModifySeqProperty(OOTCutsceneCommon, PropertyGroup):
    attrName = "mod_seq_list"
    subprops = ["mod_seq_type", "startFrame"]

    mod_seq_type: EnumProperty(name="", items=lambda self, context: game_data.z64.get_enum("mod_seq_type"), default=1)
    mod_seq_type_custom: StringProperty("CS_MOD_SEQ_CUSTOM")


class OOTCSListProperty(PropertyGroup):
    expandTab: BoolProperty(default=True)

    listType: EnumProperty(items=lambda self, context: game_data.z64.get_enum("cs_list_type"))
    textList: CollectionProperty(type=OOTCSTextProperty)
    lightSettingsList: CollectionProperty(type=OOTCSLightSettingsProperty)
    timeList: CollectionProperty(type=OOTCSTimeProperty)
    seqList: CollectionProperty(type=OOTCSSeqProperty)
    miscList: CollectionProperty(type=OOTCSMiscProperty)
    rumbleList: CollectionProperty(type=OOTCSRumbleProperty)
    transition_list: CollectionProperty(type=OOTCSTransitionProperty)
    motion_blur_list: CollectionProperty(type=OOTCSMotionBlurProperty)
    trans_general_list: CollectionProperty(type=OOTCSTransitionGeneralProperty)
    credits_scene_list: CollectionProperty(type=OOTCSChooseCreditsSceneProperty)
    mod_seq_list: CollectionProperty(type=OOTCSModifySeqProperty)

    def draw_props(self, layout: UILayout, listIndex: int, objName: str, collectionType: str):
        box = layout.box().column()
        list_type_enum = game_data.z64.get_enum("cs_list_type")
        enumName = getEnumName(list_type_enum, self.listType)

        # Draw current command tab
        box.prop(
            self,
            "expandTab",
            text=enumName,
            icon="TRIA_DOWN" if self.expandTab else "TRIA_RIGHT",
        )

        if not self.expandTab:
            return

        drawCollectionOps(box, listIndex, collectionType, None, objName, False)

        # Draw current command content
        if self.listType == "TextList":
            attrName = "textList"
        elif self.listType == "Transition":
            attrName = "transition_list"
        elif self.listType == "LightSettingsList":
            attrName = "lightSettingsList"
        elif self.listType == "TimeList":
            attrName = "timeList"
        elif self.listType in ["StartSeqList", "StopSeqList", "FadeOutSeqList"]:
            attrName = "seqList"
        elif self.listType == "MiscList":
            attrName = "miscList"
        elif self.listType == "RumbleList":
            attrName = "rumbleList"
        elif self.listType == "MotionBlurList":
            attrName = "motion_blur_list"
        elif self.listType == "TransitionGeneralList":
            attrName = "trans_general_list"
        elif self.listType == "CreditsSceneList":
            attrName = "credits_scene_list"
        elif self.listType == "ModifySeqList":
            attrName = "mod_seq_list"
        else:
            raise PluginError("Internal error: invalid listType " + self.listType)

        data = getattr(self, attrName)

        if self.listType == "TextList":
            subBox = box.box()
            subBox.label(text="TextBox Commands")
            row = subBox.row(align=True)

            for l in range(3):
                addOp = row.operator(
                    OOTCSTextAdd.bl_idname,
                    text="Add " + ootEnumCSTextboxType[l][1],
                    icon=ootEnumCSTextboxTypeIcons[ootEnumCSTextboxType[l][0]],
                )

                addOp.collectionType = collectionType + ".textList"
                addOp.textboxType = ootEnumCSTextboxType[l][0]
                addOp.listIndex = listIndex
                addOp.objName = objName
        else:
            addOp = box.operator(
                OOTCollectionAdd.bl_idname, text="Add item to " + getEnumName(list_type_enum, self.listType)
            )
            addOp.option = len(data)
            addOp.collectionType = collectionType + "." + attrName
            addOp.subIndex = listIndex
            addOp.objName = objName

        for i, p in enumerate(data):
            # ``p`` type:
            # OOTCSTextProperty | OOTCSLightSettingsProperty | OOTCSTimeProperty |
            # OOTCSSeqProperty | OOTCSMiscProperty | OOTCSRumbleProperty | OOTCSTransitionProperty
            p.draw_props(box, self, listIndex, i, objName, collectionType, enumName.removesuffix(" List"))

        if len(data) == 0:
            box.label(text="No items in " + getEnumName(list_type_enum, self.listType))


class OOTCutsceneCommandBase:
    startFrame: IntProperty(min=0)
    endFrame: IntProperty(min=0)


class OOTCutsceneTransitionProperty(OOTCutsceneCommandBase, PropertyGroup):
    type: StringProperty(default="Unknown")


class OOTCutsceneMiscProperty(OOTCutsceneCommandBase, PropertyGroup):
    type: StringProperty(default="Unknown")


class OOTCutscenePreviewProperty(PropertyGroup):
    transitionList: CollectionProperty(type=OOTCutsceneTransitionProperty)
    miscList: CollectionProperty(type=OOTCutsceneMiscProperty)

    trigger: BoolProperty(default=False)  # for ``CS_TRANS_TRIGGER_INSTANCE``
    isFixedCamSet: BoolProperty(default=False)
    prevFrame: IntProperty(default=-1)
    nextFrame: IntProperty(default=1)


class OOTCutscenePreviewSettingsProperty(PropertyGroup):
    useWidescreen: BoolProperty(
        name="Use Widescreen Camera", default=False, update=lambda self, context: self.updateWidescreen(context)
    )

    useOpaqueCamBg: BoolProperty(
        name="Use Opaque Camera Background",
        description="Can be used to simulate the letterbox with widescreen mode enabled",
        default=False,
        update=lambda self, context: self.updateCamBackground(context),
    )

    previewPlayerAge: EnumProperty(
        items=[("link_adult", "Adult", "Adult Link (170 cm)", 0), ("link_child", "Child", "Child Link (130 cm)", 1)],
        name="Player Age for Preview",
        description="For setting Link's height for preview",
        default="link_adult",
    )

    # internal only
    ootCSPreviewNodesReady: BoolProperty(default=False)
    ootCSPreviewCSObj: PointerProperty(type=Object)

    def updateWidescreen(self, context: Context):
        if self.useWidescreen:
            context.scene.render.resolution_x = 426
        else:
            context.scene.render.resolution_x = 320
        context.scene.render.resolution_y = 240

        # force a refresh of the current frame
        previewFrameHandler(context.scene)

    def updateCamBackground(self, context: Context):
        camObj = getCutsceneCamera(context.view_layer.objects.active)
        if camObj is not None:
            if self.useOpaqueCamBg:
                camObj.data.passepartout_alpha = 1.0
            else:
                camObj.data.passepartout_alpha = 0.95

    def draw_props(self, layout: UILayout):
        previewBox = layout.box()
        previewBox.box().label(text="Preview Settings")
        prop_split(previewBox, self, "previewPlayerAge", "Player Age for Preview")
        previewBox.prop(self, "useWidescreen")
        previewBox.prop(self, "useOpaqueCamBg")


class OOTCutsceneProperty(PropertyGroup):
    csEndFrame: IntProperty(name="End Frame", min=0, default=100)
    csUseDestination: BoolProperty(name="Cutscene Destination (Scene Change)")
    csDestination: EnumProperty(
        name="Destination", items=lambda self, context: game_data.z64.get_enum("csDestination"), default=1
    )
    csDestinationCustom: StringProperty(default="CS_DEST_CUSTOM")
    csDestinationStartFrame: IntProperty(name="Start Frame", min=0, default=99)
    cs_give_tatl: BoolProperty(name="Give Tatl")
    cs_give_tatl_start_frame: IntProperty(name="Start Frame", min=0, default=99)
    csLists: CollectionProperty(type=OOTCSListProperty, name="Cutscene Lists")
    next_entrance: StringProperty(default="0xFFFF")
    play_on_spawn: IntProperty(min=0, default=0)
    spawn_flag_type: EnumProperty(
        items=[
            ("Custom", "Custom", "Custom"),
            ("CS_SPAWN_FLAG_NONE", "None", "None"),
            ("CS_SPAWN_FLAG_ALWAYS", "Always", "Always"),
            ("CS_SPAWN_FLAG_ONCE", "Flag", "Flag"),
        ],
        default=2,
    )
    spawn_flag: StringProperty(default="0x00")
    spawn_flags_custom: StringProperty(default="CS_SPAWN_FLAG_CUSTOM")

    menuTab: EnumProperty(items=lambda self, context: game_data.z64.get_enum("cs_list_type"))
    preview: PointerProperty(type=OOTCutscenePreviewProperty)

    @staticmethod
    def upgrade_object(obj):
        print(f"Processing '{obj.name}'...")

        # using the new names since the old ones will be deleted before this is used
        csListsNames = ["textList", "lightSettingsList", "timeList", "seqList", "miscList", "rumbleList"]

        csProp: "OOTCutsceneProperty" = obj.ootCutsceneProperty
        upgradeCutsceneProperty(csProp)

        for csListProp in csProp.csLists:
            upgradeCSListProps(csListProp)

            for listName in csListsNames:
                for csListSubProp in getattr(csListProp, listName):
                    upgradeCutsceneSubProps(csListSubProp)

            if csListProp.listType == "Transition":
                new_entry = csListProp.transition_list.add()

                if "transitionType" in csListProp:
                    new_entry.transition_type = csListProp.transitionType
                    del csListProp["transitionType"]
                if "transitionTypeCustom" in csListProp:
                    new_entry.transition_type_custom = csListProp.transitionTypeCustom
                    del csListProp["transitionTypeCustom"]
                if "transitionStartFrame" in csListProp:
                    new_entry.startFrame = csListProp.transitionStartFrame
                    del csListProp["transitionStartFrame"]
                if "transitionEndFrame" in csListProp:
                    new_entry.endFrame = csListProp.transitionEndFrame
                    del csListProp["transitionEndFrame"]

    def draw_props(self, layout: UILayout, obj: Object):
        layout = layout.column()
        split = layout.split(factor=0.5)
        split.operator(CutsceneCmdCreateCameraShot.bl_idname, icon="VIEW_CAMERA")
        split.operator(CutsceneCmdPlayPreview.bl_idname, icon="RESTRICT_VIEW_OFF")

        split = layout.split(factor=0.5)
        split.operator(CutsceneCmdCreatePlayerCueList.bl_idname)
        split.operator(CutsceneCmdCreateActorCueList.bl_idname)

        split = layout.split(factor=0.5)
        split.label(text="Cutscene End Frame")
        split.prop(self, "csEndFrame")

        if game_data.z64.is_mm() or not is_oot_features():
            prop_split(layout, self, "next_entrance", "Next Entrance")
            prop_split(layout, self, "play_on_spawn", "Spawn")
            prop_split(layout, self, "spawn_flag_type", "Spawn Flags")

            if self.spawn_flag_type == "Custom":
                prop_split(layout, self, "spawn_flags_custom", "")

            if self.spawn_flag_type == "CS_SPAWN_FLAG_ONCE":
                prop_split(layout, self, "spawn_flag", "")

        commandsBox = layout.box()
        commandsBox.box().label(text="Cutscene Commands")

        b = commandsBox.box()
        b.prop(self, "csUseDestination")
        if self.csUseDestination:
            b.prop(self, "csDestinationStartFrame")

            if game_data.z64.is_oot():
                searchBox = b.box()
                boxRow = searchBox.row()
                searchOp = boxRow.operator(OOT_SearchCSDestinationEnumOperator.bl_idname, icon="VIEWZOOM", text="")
                searchOp.objName = obj.name
                boxRow.label(text=getEnumName(game_data.z64.get_enum("csDestination"), self.csDestination))
                layout_custom = searchBox
            else:
                layout_custom = b
                prop_split(b, self, "csDestination", "Cutscene Destination Type")

            if self.csDestination == "Custom":
                prop_split(layout_custom.column(), self, "csDestinationCustom", "Cutscene Destination Custom")

        b = commandsBox.box()
        b.prop(self, "cs_give_tatl")
        if self.cs_give_tatl:
            b.prop(self, "cs_give_tatl_start_frame")

        commandsBox.column_flow(columns=3, align=True).prop(self, "menuTab", expand=True)
        label = f"Add New {ootCSSubPropToName[self.menuTab]}"
        op = commandsBox.operator(OOTCSListAdd.bl_idname, text=label, icon=csListTypeToIcon[self.menuTab])
        op.collectionType = "Cutscene"
        op.listType = self.menuTab
        op.objName = obj.name

        for i, csListProp in enumerate(self.csLists):
            # ``csListProp`` type: OOTCSListProperty
            if csListProp.listType == self.menuTab:
                csListProp.draw_props(commandsBox, i, obj.name, "Cutscene")


classes = (
    OOTCSTextProperty,
    OOTCSLightSettingsProperty,
    OOTCSTimeProperty,
    OOTCSSeqProperty,
    OOTCSMiscProperty,
    OOTCSRumbleProperty,
    OOTCSTransitionProperty,
    OOTCSMotionBlurProperty,
    OOTCSTransitionGeneralProperty,
    OOTCSChooseCreditsSceneProperty,
    OOTCSModifySeqProperty,
    OOTCSListProperty,
    OOTCutsceneTransitionProperty,
    OOTCutsceneMiscProperty,
    OOTCutscenePreviewProperty,
    OOTCutscenePreviewSettingsProperty,
    OOTCutsceneProperty,
)


def cutscene_props_register():
    game_data.z64.update(None, "OOT", True)

    for cls in classes:
        register_class(cls)

    Object.ootCutsceneProperty = PointerProperty(type=OOTCutsceneProperty)
    Scene.ootPreviewSettingsProperty = PointerProperty(type=OOTCutscenePreviewSettingsProperty)


def cutscene_props_unregister():
    del Scene.ootPreviewSettingsProperty
    del Object.ootCutsceneProperty

    for cls in reversed(classes):
        unregister_class(cls)
