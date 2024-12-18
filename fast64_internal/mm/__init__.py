import bpy

from bpy.utils import register_class, unregister_class
from bpy.types import Context, UILayout
from ..utility import prop_split

from .file_settings import file_register, file_unregister
from .f3d.panels import f3d_panels_register, f3d_panels_unregister

# module imports
from .constants import mm_world_defaults


class MM_Properties(bpy.types.PropertyGroup):
    """Global MM Scene Properties found under scene.fast64.mm"""

    version: bpy.props.IntProperty(name="MM_Properties Version", default=0)
    use_decomp_features: bpy.props.BoolProperty(
        name="Use decomp for export", description="Use names and macros from decomp when exporting", default=True
    )


mm_classes = (MM_Properties,)


def mm_panel_register():
    file_register()
    f3d_panels_register()


def mm_panel_unregister():
    f3d_panels_unregister()
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
