from bpy.utils import register_class, unregister_class
from bpy.props import StringProperty, FloatProperty, BoolProperty
from bpy.types import Scene
from ..utility import prop_split
from ..render_settings import on_update_render_settings
from ..panels import Z64_Panel


class WorkspaceSettings(Z64_Panel):
    bl_idname = "Z64_PT_workspace_settings"
    bl_label = "Workspace Settings"
    bl_options = set()

    def draw(self, context):
        col = self.layout.column()
        col.scale_y = 1.1  # extra padding, makes it easier to see these main settings

        prop_split(col, context.scene, "z64_blender_scale", "Scene Scale")
        prop_split(col, context.scene, "z64_decomp_path", "Decomp Path")
        context.scene.fast64.z64.draw(col)


oot_classes = (WorkspaceSettings,)


def file_register():
    for cls in oot_classes:
        register_class(cls)

    Scene.z64_blender_scale = FloatProperty(name="Blender To Z64 Scale", default=10, update=on_update_render_settings)
    Scene.z64_decomp_path = StringProperty(name="Decomp Folder", subtype="FILE_PATH")


def file_unregister():
    for cls in reversed(oot_classes):
        unregister_class(cls)

    del Scene.z64_blender_scale
    del Scene.z64_decomp_path
