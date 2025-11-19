import re
import traceback

from pathlib import Path
from typing import Optional

from bpy.utils import register_class, unregister_class
from bpy.props import IntProperty, BoolProperty, StringProperty, EnumProperty, PointerProperty
from bpy.types import Operator

from ...game_data import game_data
from ...f3d.f3d_parser import getImportData
from ..utility import ootGetObjectPath, ootGetObjectHeaderPath
from ..tools.quick_import import quick_import_exec
from ..importer.scene_collision import parseCollisionHeader
from ..importer.utility import SharedSceneData

# Note: in this context "object" means a game object


class Z64_SearchObjectEnumOperator(Operator):
    bl_idname = "object.z64_search_object_enum_operator"
    bl_label = "Choose Object"
    bl_property = "object_key"
    bl_options = {"REGISTER", "UNDO"}

    object_key: EnumProperty(items=lambda self, context: game_data.z64.get_enum("object_key"), default=1)
    mode: StringProperty(default="Export")

    def execute(self, context):
        if self.mode == "Export":
            context.scene.fast64.oot.object_export_settings.object_key = self.object_key
        elif self.mode == "Import":
            context.scene.fast64.oot.object_import_settings.object_key = self.object_key
        # elif self.mode == "Remove":
        #     context.scene.ootSceneRemoveSettings.option = self.ootSceneID
        else:
            raise Exception(f"ERROR: unknown operation mode: {repr(self.mode)}")

        context.region.tag_redraw()
        self.report({"INFO"}, f"Selected: {self.object_key}")
        return {"FINISHED"}

    def invoke(self, context, _):
        context.window_manager.invoke_search_popup(self)
        return {"RUNNING_MODAL"}


class Z64_ExportObject(Operator):
    bl_idname = "object.z64_export_object_operator"
    bl_label = "Export Object"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        self.report({"INFO"}, "Success!")
        return {"FINISHED"}


class Z64_ImportObject(Operator):
    bl_idname = "object.z64_import_object_operator"
    bl_label = "Import Object"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from .properties import Z64_ObjectImportSettings

        settings: Z64_ObjectImportSettings = context.scene.fast64.oot.object_import_settings
        decomp_path = Path(context.scene.ootDecompPath)
        include_extracted = False

        if settings.is_custom_path:
            folder_name = settings.custom_name
            import_path = settings.custom_path
        else:
            folder_name = game_data.z64.objects.objects_by_key[settings.object_key].id.lower()
            import_path = f"assets/objects/{folder_name}"
            filename = f"{import_path}/{folder_name}.c"

            if not (decomp_path / filename).exists():
                include_extracted = True

        paths = [
            ootGetObjectPath(settings.is_custom_path, import_path, folder_name, include_extracted),
            ootGetObjectHeaderPath(settings.is_custom_path, import_path, folder_name, include_extracted),
        ]

        if not include_extracted:
            paths.extend(
                [
                    ootGetObjectPath(settings.is_custom_path, import_path, folder_name, True),
                    ootGetObjectHeaderPath(settings.is_custom_path, import_path, folder_name, True),
                ]
            )

        filedata = getImportData(paths)
        symbols: list[str] = []
        regex_list: list[str] = []

        if settings.include_dl:
            regex_list.append(r"Gfx\s*([a-zA-Z0-9_]*)\[[a-zA-Z0-9_]*\]\s*=\s*\{")

        if settings.include_collision:
            col_syms = re.findall(r"CollisionHeader\s*([a-zA-Z0-9_]*)\s*=\s*\{", filedata, re.DOTALL)

            # TODO: temporary thing to import collision, should be moved elsewhere
            shared_scene_data = SharedSceneData(
                import_path,
                folder_name,
                True,
                True,
                False,
                False,
                False,
                False,
                True,
                False,
                False,
                False,
                True,
                False,
                ".inc.c" in filedata,
            )

            for sym in col_syms:
                parseCollisionHeader(None, [], filedata, sym, shared_scene_data, sym)

        if settings.include_skeletons:
            regex_list.extend(
                [r"FlexSkeletonHeader\s*([a-zA-Z0-9_]*)\s*=\s*\{", r"SkeletonHeader\s*([a-zA-Z0-9_]*)\s*=\s*\{"]
            )

        for regex in regex_list:
            symbols.extend(re.findall(regex, filedata, re.DOTALL))

        # remove duplicates
        symbols = list(set(symbols))

        for sym_name in symbols:
            try:
                quick_import_exec(context, sym_name)
            except:
                print(f"WARNING: importing '{sym_name}' from object '{folder_name}' ('{import_path}') failed with:")
                traceback.print_exc()

        self.report({"INFO"}, "Success!")
        return {"FINISHED"}


ops_classes = (
    Z64_SearchObjectEnumOperator,
    Z64_ExportObject,
    Z64_ImportObject,
)


def object_ops_register():
    for cls in ops_classes:
        register_class(cls)


def object_ops_unregister():
    for cls in reversed(ops_classes):
        unregister_class(cls)
