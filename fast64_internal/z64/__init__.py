import bpy

from bpy.utils import register_class, unregister_class
from bpy.types import Context, UILayout
from ..utility import prop_split
from .f3d.operators import f3d_ops_register, f3d_ops_unregister
from .f3d.properties import Z64_DLExportSettings, Z64_DLImportSettings, f3d_props_register, f3d_props_unregister
from .utility import test_game_type
from .workspace import file_register, file_unregister


oot_versions_items = [
    ("Custom", "Custom", "Custom"),
    ("gc-jp", "gc-jp", "gc-jp"),
    ("gc-jp-mq", "gc-jp-mq", "gc-jp-mq"),
    ("gc-jp-ce", "gc-jp-ce", "gc-jp-ce"),
    ("gc-us", "gc-us", "gc-us"),
    ("gc-us-mq", "gc-us-mq", "gc-us-mq"),
    ("gc-eu", "gc-eu", "gc-eu"),
    ("gc-eu-mq", "gc-eu-mq", "gc-eu-mq"),
    ("gc-eu-mq-dbg", "gc-eu-mq-dbg", "gc-eu-mq-dbg"),
    ("hackeroot-mq", "HackerOoT", "hackeroot-mq"),  # TODO: force this value if HackerOoT features are enabled?
    ("legacy", "Legacy", "Older Decomp Version"),
]


mm_versions_items = [
    ("Custom", "Custom", "Custom"),
    ("n64-us", "n64-us", "n64-us"),
    ("legacy", "Legacy", "Older Decomp Version"),
]


class Z64_Properties(bpy.types.PropertyGroup):
    """Global Zelda64 Scene Properties found under scene.fast64.z64"""

    version: bpy.props.IntProperty(name="Z64_Properties Version", default=0)

    DLExportSettings: bpy.props.PointerProperty(type=Z64_DLExportSettings)
    DLImportSettings: bpy.props.PointerProperty(type=Z64_DLImportSettings)

    oot_version: bpy.props.EnumProperty(name="OoT Version", items=oot_versions_items, default="gc-eu-mq-dbg")
    mm_version: bpy.props.EnumProperty(name="MM Version", items=mm_versions_items, default="n64-us")
    z64_version_custom: bpy.props.StringProperty(name="Custom Version")

    def get_version(self):
        return self.oot_version if test_game_type("OOT") else self.mm_version

    def get_extracted_path(self):
        z64_version = self.get_version()

        if z64_version == "legacy":
            return "."
        else:
            return f"extracted/{z64_version if z64_version != 'Custom' else self.z64_version_custom}"

    def draw(self, layout: UILayout):
        if test_game_type("OOT"):
            prop_split(layout, self, "oot_version", "Version")
        else:
            prop_split(layout, self, "mm_version", "Version")

        if self.get_version() == "Custom":
            prop_split(layout, self, "z64_version_custom", "Custom Version")


z64_classes = (Z64_Properties,)


def z64_panel_register():
    pass


def z64_panel_unregister():
    pass


def z64_register(registerPanels):
    f3d_props_register()
    f3d_ops_register()
    file_register()

    for cls in z64_classes:
        register_class(cls)

    if registerPanels:
        z64_panel_register()


def z64_unregister(unregisterPanels):
    for cls in reversed(z64_classes):
        unregister_class(cls)

    file_unregister()
    f3d_props_unregister()
    f3d_ops_unregister()

    if unregisterPanels:
        z64_panel_unregister()
