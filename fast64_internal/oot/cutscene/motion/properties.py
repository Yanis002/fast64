import bpy

from bpy.ops import object
from bpy.types import PropertyGroup, Object, UILayout, Armature, Bone, Scene, EditBone
from bpy.props import IntProperty, StringProperty, PointerProperty, EnumProperty, FloatProperty
from bpy.utils import register_class, unregister_class
from ...oot_upgrade import upgradeCutsceneMotion
from ...oot_utility import getEnumName
from .constants import ootEnumCSMotionCamMode, ootEnumCSActorCueListCommandType

from .operators import (
    OOTCSMotionAddActorCue,
    OOTCSMotionCreateActorCuePreview,
    OOT_SearchActorCueCmdTypeEnumOperator,
    OOTCSMotionAddBone,
)


def getNextCuesStartFrame(self):
    curCueObj = bpy.context.view_layer.objects.active
    parentObj = curCueObj.parent

    if parentObj is not None and parentObj.ootEmptyType in ["CS Actor Cue List", "CS Player Cue List"]:
        if curCueObj.ootEmptyType in ["CS Actor Cue", "CS Player Cue"]:
            actorCueObjList = parentObj.children
            for i, obj in enumerate(actorCueObjList):
                if obj == curCueObj:
                    return actorCueObjList[i + 1].ootCSMotionProperty.actorCueProp.cueStartFrame
    return -1


class OOTCSMotionActorCueListProperty(PropertyGroup):
    commandType: EnumProperty(
        items=ootEnumCSActorCueListCommandType, name="CS Actor Cue Command Type", default="0x000F"
    )
    commandTypeCustom: StringProperty(name="CS Actor Cue Command Type Custom")
    actorCueListToPreview: PointerProperty(
        type=Object, name="", poll=lambda self, object: self.isActorCueListObj(object, "CS Actor Cue List")
    )
    playerCueListToPreview: PointerProperty(
        type=Object, name="", poll=lambda self, object: self.isActorCueListObj(object, "CS Player Cue List")
    )

    def isActorCueListObj(self, obj: Object, emptyType: str):
        return obj.type == "EMPTY" and obj.ootEmptyType == emptyType

    def draw_props(self, layout: UILayout, isPreview: bool, labelPrefix: str, objName: str):
        box = layout.box()
        box.box().label(text=f"{labelPrefix} Cue List")
        isPlayer = labelPrefix == "Player"

        # Player Cue has only one command type
        if not isPlayer and not isPreview:
            searchBox = box.row()
            searchOp = searchBox.operator(
                OOT_SearchActorCueCmdTypeEnumOperator.bl_idname, icon="VIEWZOOM", text="Command Type:"
            )
            searchOp.objName = objName
            searchBox.label(text=getEnumName(ootEnumCSActorCueListCommandType, self.commandType))

            if self.commandType == "Custom":
                split = box.split(factor=0.5)
                split.label(text="Command Type Custom:")
                split.prop(self, "commandTypeCustom", text="")

        if not isPreview:
            split = box.split(factor=0.5)
            addCueOp = split.operator(OOTCSMotionAddActorCue.bl_idname, text=f"Add {labelPrefix} Cue")
            addCueOp.isPlayer = isPlayer
            split.operator(OOTCSMotionCreateActorCuePreview.bl_idname)
        else:
            split = box.split(factor=0.5)
            split.label(text=f"{labelPrefix} Cue List to Preview")
            split.prop(self, f"{labelPrefix.lower()}CueListToPreview")


class OOTCSMotionActorCueProperty(PropertyGroup):
    cueStartFrame: IntProperty(name="Start Frame", description="Start frame of the Actor Cue", default=0, min=0)

    cueEndFrame: IntProperty(
        name="End Frame",
        description="End Frame of the Actor Cue, corresponds to the Start Frame of the next Actor Cue",
        default=0,
        min=-1,
        get=lambda self: getNextCuesStartFrame(self),
    )

    cueActionID: StringProperty(
        name="Action ID", default="0x0001", description="Actor action. Meaning is unique for each different actor."
    )

    def draw_props(self, layout: UILayout, labelPrefix: str, isDummy: bool):
        box = layout.box()
        dummyExtra = "(Sets previous Actor Cue's end frame/pos.)" if isDummy else ""
        boxBox = box.box()
        boxBox.label(text=f"{labelPrefix if not isDummy else 'Dummy'} Cue")
        if len(dummyExtra) > 0:
            boxBox.label(text=dummyExtra)

        if not isDummy and self.cueStartFrame > self.cueEndFrame:
            box.label(
                text="Warning: Start Frame > End Frame!",
                icon="ERROR",
            )

        split = box.split(factor=0.5)
        split.prop(self, "cueStartFrame")
        if not isDummy:
            split.prop(self, "cueEndFrame")

            split = box.split(factor=0.5)
            split.label(text=f"{labelPrefix} Cue (Action) ID")
            split.prop(self, "cueActionID", text="")
            addCueOp = box.operator(OOTCSMotionAddActorCue.bl_idname, text=f"Add {labelPrefix} Cue")
            addCueOp.isPlayer = labelPrefix == "Player"


class OOTCSMotionCameraShotProperty(PropertyGroup):
    shotStartFrame: IntProperty(name="Start Frame", description="Shot start frame", default=0, min=0)
    shotCamMode: EnumProperty(
        items=ootEnumCSMotionCamMode,
        name="Mode",
        description="Camera command mode",
        default="splineEyeOrAT",
    )

    def draw_props(self, layout: UILayout, label: str):
        box = layout.box()
        box.label(text=label)
        box.prop(self, "shotStartFrame")
        box.row().prop(self, "shotCamMode", expand=True)
        box.operator(OOTCSMotionAddBone.bl_idname)


class OOTCSMotionCameraShotPointProperty(PropertyGroup):
    shotPointFrame: IntProperty(
        name="Frame",
        description="Key point frames value",
        default=30,
        min=0,
        get=lambda self: self.getValue("frame"),
        set=lambda self, value: self.setValue(value, "frame"),
    )

    shotPointViewAngle: FloatProperty(
        name="FoV",
        description="Field of view (degrees)",
        default=60.0,
        min=0.01,
        max=179.99,
        get=lambda self: self.getValue("viewAngle"),
        set=lambda self, value: self.setValue(value, "viewAngle"),
    )

    shotPointRoll: IntProperty(
        name="Roll",
        description="Camera roll (degrees), positive turns image clockwise",
        default=0,
        min=-128,
        max=127,
        get=lambda self: self.getValue("roll"),
        set=lambda self, value: self.setValue(value, "roll"),
    )

    # internal usage only
    frame: IntProperty(default=30, min=0)
    viewAngle: FloatProperty(default=60.0, min=0.01, max=179.99)
    roll: IntProperty(min=-128, max=127, default=0)

    def getBoneFromEditBone(self, shotObject: Object, editBone: EditBone) -> Bone | None:
        for bone in shotObject.data.bones:
            if bone.name == editBone.name:
                return bone
        else:
            print("Could not find corresponding bone")
            return None

    def getValue(self, propName: str):
        return getattr(self, propName)

    def setValue(self, value, propName: str):
        setattr(self, propName, value)

        activeObj = bpy.context.view_layer.objects.active
        if activeObj.mode == "EDIT":
            bone = self.getBoneFromEditBone(activeObj, activeObj.data.edit_bones.active)
            if bone is not None:
                setattr(bone.ootCamShotPointProp, propName, value)
                activeObj.data.bones.active = bone

    def draw_props(self, layout: UILayout):
        box = layout.box()
        box.label(text="Bone / Key point:")
        row = box.row()
        for propName in ["shotPointFrame", "shotPointViewAngle", "shotPointRoll"]:
            row.prop(self, propName)


class OOTCutsceneMotionProperty(PropertyGroup):
    actorCueListProp: PointerProperty(type=OOTCSMotionActorCueListProperty)
    actorCueProp: PointerProperty(type=OOTCSMotionActorCueProperty)

    @staticmethod
    def upgrade_object(csObj: Object):
        print(f"Processing '{csObj.name}'...")
        upgradeCutsceneMotion(csObj)
        print("Done!")


classes = (
    OOTCSMotionActorCueListProperty,
    OOTCSMotionActorCueProperty,
    OOTCSMotionCameraShotProperty,
    OOTCSMotionCameraShotPointProperty,
    OOTCutsceneMotionProperty,
)


def csMotion_props_register():
    for cls in classes:
        register_class(cls)

    Object.ootCSMotionProperty = PointerProperty(type=OOTCutsceneMotionProperty)
    Armature.ootCamShotProp = PointerProperty(type=OOTCSMotionCameraShotProperty)
    Bone.ootCamShotPointProp = PointerProperty(type=OOTCSMotionCameraShotPointProperty)
    EditBone.ootCamShotPointProp = PointerProperty(type=OOTCSMotionCameraShotPointProperty)
    Scene.previewPlayerAge = EnumProperty(
        items=[("link_adult", "Adult", "Adult Link (170 cm)", 0), ("link_child", "Child", "Child Link (130 cm)", 1)],
        name="Player Age for Preview",
        description="For setting Link's height for preview",
        default="link_adult",
    )


def csMotion_props_unregister():
    del Scene.previewPlayerAge
    del EditBone.ootCamShotPointProp
    del Bone.ootCamShotPointProp
    del Armature.ootCamShotProp
    del Object.ootCSMotionProperty

    for cls in classes:
        unregister_class(cls)
