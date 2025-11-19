from bpy.utils import register_class, unregister_class
from bpy.types import PropertyGroup, UILayout, Object, Context
from bpy.props import IntProperty, BoolProperty, StringProperty, EnumProperty, PointerProperty

from ...game_data import game_data
from ...utility import prop_split
from ..utility import getEnumName
from .operators import Z64_SearchObjectEnumOperator, Z64_ExportObject, Z64_ImportObject

# Note: in this context "object" means a game object


class Z64_ObjectCommonSettings(PropertyGroup):
    object_key: StringProperty(default="gameplay_keep")
    is_custom_path: BoolProperty(default=False, description="Custom path location")
    custom_path: StringProperty(description="Directory", subtype="DIR_PATH")
    custom_name: StringProperty(default="object_custom", description="Name")

    include_dl: BoolProperty(default=False)
    include_collision: BoolProperty(default=False)
    include_skeletons: BoolProperty(default=False, update=lambda self, context: self.on_skeletons_update())
    include_animations: BoolProperty(default=False, update=lambda self, context: self.on_animations_update())

    def on_skeletons_update(self):
        if self.internal_mode == "Import":
            # force skeletons to be enabled if animations are required
            if self.include_animations:
                self.include_skeletons = True

    def on_animations_update(self):
        if self.internal_mode == "Import":
            if not self.include_skeletons:
                self.include_skeletons = True

    def draw_search_op(self, layout: UILayout):
        search_box = layout.row()
        search_op = search_box.operator(Z64_SearchObjectEnumOperator.bl_idname, icon="VIEWZOOM", text="")
        search_op.mode = self.internal_mode
        search_box.label(text=getEnumName(game_data.z64.get_enum("object_key"), self.object_key))

    def draw_settings(self, layout: UILayout):
        pass

    def draw_props(self, layout: UILayout):
        layout.label(text=f"Object {self.internal_mode}")

        dest_box = layout.box().column()
        dest_box.prop(self, "is_custom_path", text=f"Custom {self.internal_mode} Path")

        if self.is_custom_path:
            prop_split(dest_box, self, "custom_path", "Custom Path")
            prop_split(dest_box, self, "custom_name", "Name")
        else:
            self.draw_search_op(dest_box)

        self.draw_settings(layout)


class Z64_ObjectExportSettings(Z64_ObjectCommonSettings):
    is_single_file: BoolProperty(default=False, description="Does not split into multiple files.")

    object: PointerProperty(
        type=Object,
        poll=lambda self, obj: self.poll(obj),
        update=lambda self, context: self.on_object_update(),
        description="Object Empty with the elements to export.",
    )

    internal_mode: StringProperty(default="Export")

    def poll(self, obj: Object):
        return obj.type == "EMPTY" and obj.ootEmptyType == "Object"

    def on_object_update(self):
        selected_obj: Object = self.object

        self.include_dl = False
        self.include_collision = False
        self.include_skeletons = False
        self.include_animations = False

        for obj in selected_obj.children_recursive:
            if obj.type == "MESH":
                self.include_dl = obj.ignore_render is False
                self.include_collision = obj.ignore_collision is False
            elif obj.type == "ARMATURE":
                self.include_skeletons = True
            else:
                print(f"WARNING: object {repr(obj.name)} won't be exported.")

    def draw_settings(self, layout):
        prop_split(layout, self, "object", "Game Object")
        layout.prop(self, "is_single_file", text="Export as Single File")
        layout.operator(Z64_ExportObject.bl_idname)


class Z64_ObjectImportSettings(Z64_ObjectCommonSettings):
    internal_mode: StringProperty(default="Import")

    def draw_settings(self, layout):
        col = layout.box().column()

        row_1 = col.row(align=True)
        row_1.prop(self, "include_dl", text="DLs", toggle=1)
        row_1.prop(self, "include_collision", text="Collision", toggle=1)
        row_1.prop(self, "include_skeletons", text="Skeletons", toggle=1)

        # TODO: uncomment when PR 485 is merged
        # row_2 = col.row(align=True)
        # row_2.prop(self, "include_animations", text="Animations", toggle=1)

        layout.operator(Z64_ImportObject.bl_idname)


props_classes = (Z64_ObjectExportSettings, Z64_ObjectImportSettings)


def object_props_register():
    for cls in props_classes:
        register_class(cls)


def object_props_unregister():
    for cls in reversed(props_classes):
        unregister_class(cls)
