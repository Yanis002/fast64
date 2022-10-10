from bpy.types import Panel, Object, Armature, Bone
from bpy.props import PointerProperty, EnumProperty, StringProperty
from bpy.utils import register_class, unregister_class
from .....utility import prop_split
from ....model import OOTDynamicTransformProperty


ootEnumBoneType = [
    ("Default", "Default", "Default"),
    ("Custom DL", "Custom DL", "Custom DL"),
    ("Ignore", "Ignore", "Ignore"),
]


class OOT_SkeletonPanel(Panel):
    bl_idname = "OOT_PT_skeleton"
    bl_label = "OOT Skeleton Properties"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return (
            context.scene.gameEditorMode == "OOT"
            and hasattr(context, "object")
            and context.object is not None
            and isinstance(context.object.data, Armature)
        )

    # called every frame
    def draw(self, context):
        col = self.layout.box().column()
        col.box().label(text="OOT Skeleton Inspector")
        prop_split(col, context.object, "ootDrawLayer", "Draw Layer")
        prop_split(col, context.object, "ootFarLOD", "LOD Skeleton")

        if context.object.ootFarLOD is not None:
            col.label(text="Make sure LOD has same bone structure.", icon="BONE_DATA")


class OOT_BonePanel(Panel):
    bl_idname = "OOT_PT_bone"
    bl_label = "OOT Bone Properties"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "bone"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return context.scene.gameEditorMode == "OOT" and context.bone is not None

    # called every frame
    def draw(self, context):
        col = self.layout.box().column()
        col.box().label(text="OOT Bone Inspector")
        prop_split(col, context.bone, "ootBoneType", "Bone Type")

        if context.bone.ootBoneType == "Custom DL":
            prop_split(col, context.bone, "ootCustomDLName", "DL Name")

        if context.bone.ootBoneType == "Custom DL" or context.bone.ootBoneType == "Ignore":
            col.label(text="Make sure no geometry is skinned to this bone.", icon="BONE_DATA")

        if context.bone.ootBoneType != "Ignore":
            col.prop(context.bone.ootDynamicTransform, "billboard")


def pollArmature(self, obj):
    return isinstance(obj.data, Armature)


oot_skeleton_panels = (
    OOT_SkeletonPanel,
    OOT_BonePanel,
)


def oot_skeleton_panel_register():
    for cls in oot_skeleton_panels:
        register_class(cls)


def oot_skeleton_panel_unregister():
    for cls in oot_skeleton_panels:
        unregister_class(cls)


def oot_skeleton_register():
    Object.ootFarLOD = PointerProperty(type=Object, poll=pollArmature)

    Bone.ootBoneType = EnumProperty(name="Bone Type", items=ootEnumBoneType)
    Bone.ootDynamicTransform = PointerProperty(type=OOTDynamicTransformProperty)
    Bone.ootCustomDLName = StringProperty(name="Custom DL", default="gEmptyDL")


def oot_skeleton_unregister():
    del Object.ootFarLOD

    del Bone.ootBoneType
    del Bone.ootDynamicTransform
    del Bone.ootCustomDLName
