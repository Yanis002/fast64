from bpy.utils import register_class, unregister_class
from bpy.props import StringProperty, FloatProperty
from bpy.types import Scene
from ..utility import prop_split
from ..render_settings import on_update_render_settings
from ..panels import MM_Panel


class MM_FileSettingsPanel(MM_Panel):
    bl_idname = "MM_PT_file_settings"
    bl_label = "File Settings"
    bl_options = set()  # default to being open

    # called every frame
    def draw(self, context):
        col = self.layout.column()
        col.scale_y = 1.1  # extra padding, makes it easier to see these main settings

        prop_split(col, context.scene, "mm_blender_scale", "MM Scene Scale")
        prop_split(col, context.scene, "mm_decomp_path", "Decomp Path")

        context.scene.fast64.mm.draw(context, col)


mm_classes = (MM_FileSettingsPanel,)


def file_register():
    for cls in mm_classes:
        register_class(cls)

    Scene.mm_blender_scale = FloatProperty(name="Blender To MM Scale", default=10, update=on_update_render_settings)
    Scene.mm_decomp_path = StringProperty(name="Decomp Folder", subtype="FILE_PATH")


def file_unregister():
    for cls in reversed(mm_classes):
        unregister_class(cls)

    del Scene.mm_blender_scale
    del Scene.mm_decomp_path
