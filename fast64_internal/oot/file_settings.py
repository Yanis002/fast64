from bpy.utils import register_class, unregister_class
from bpy.props import StringProperty, FloatProperty, BoolProperty
from bpy.types import Scene
from ..utility import prop_split
from ..render_settings import on_update_render_settings
from ..panels import OOT_Panel


class OOT_FileSettingsPanel(OOT_Panel):
    bl_idname = "OOT_PT_file_settings"
    bl_label = "OOT File Settings"
    bl_options = set()  # default to being open

    # called every frame
    def draw(self, context):
        col = self.layout.column()
        col.scale_y = 1.1  # extra padding, makes it easier to see these main settings

        col.prop(context.scene.fast64.oot, "headerTabAffectsVisibility")
        col.prop(context.scene.fast64.oot, "hackerFeaturesEnabled")

        if not context.scene.fast64.oot.hackerFeaturesEnabled:
            col.prop(context.scene.fast64.oot, "useDecompFeatures")
        col.prop(context.scene.fast64.oot, "exportMotionOnly")


oot_classes = (OOT_FileSettingsPanel,)


def file_register():
    for cls in oot_classes:
        register_class(cls)


def file_unregister():
    for cls in reversed(oot_classes):
        unregister_class(cls)
