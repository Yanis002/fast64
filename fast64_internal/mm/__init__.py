import bpy

from bpy.utils import register_class, unregister_class
from bpy.types import Context, UILayout
from ..utility import prop_split
from .file_settings import file_register, file_unregister

# module imports
from .constants import mm_world_defaults


mm_versions_items = [
    ("Custom", "Custom", "Custom"),
    ("n64-us", "n64-us", "n64-us"),
    ("legacy", "Legacy", "Older Decomp Version"),
]


class MM_Properties(bpy.types.PropertyGroup):
    """Global MM Scene Properties found under scene.fast64.mm"""

    version: bpy.props.IntProperty(name="MM_Properties Version", default=0)
    mm_version: bpy.props.EnumProperty(name="MM Version", items=mm_versions_items, default="n64-us")
    mm_version_custom: bpy.props.StringProperty(name="Custom Version")
    use_decomp_features: bpy.props.BoolProperty(
        name="Use decomp for export", description="Use names and macros from decomp when exporting", default=True
    )

    def get_extracted_path(self):
        if self.mm_version == "legacy":
            return "."
        else:
            return f"extracted/{self.mm_version if self.mm_version != 'Custom' else self.mm_version_custom}"

    def draw(self, context: Context, layout: UILayout):
        prop_split(layout, context.scene.fast64.mm, "mm_version", "MM Version")

        if context.scene.fast64.mm.mm_version == "Custom":
            prop_split(layout, context.scene.fast64.mm, "mm_version_custom", "Custom Version")


mm_classes = (MM_Properties,)


def mm_panel_register():
    file_register()


def mm_panel_unregister():
    file_unregister()


def mm_register(register_panels: bool):
    for cls in mm_classes:
        register_class(cls)

    if register_panels:
        mm_panel_register()


def mm_unregister(unregister_panels: bool):
    for cls in reversed(mm_classes):
        unregister_class(cls)

    if unregister_panels:
        mm_panel_unregister()
