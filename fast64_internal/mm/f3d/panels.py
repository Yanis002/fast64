import bpy
from bpy.types import Panel, Mesh, Armature
from bpy.utils import register_class, unregister_class
from ...panels import MM_Panel
from ...utility import prop_split
from ...z64.f3d.operators import OOT_ImportDL, OOT_ExportDL
from ...z64.f3d.properties import (
    Z64_DLExportSettings,
    Z64_DLImportSettings,
    OOTDynamicMaterialProperty,
    OOTDefaultRenderModesProperty,
)


class MM_DisplayListPanel(Panel):
    bl_label = "Display List Inspector"
    bl_idname = "OBJECT_PT_MM_DL_Inspector"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return context.scene.gameEditorMode == "MM" and (
            context.object is not None and isinstance(context.object.data, Mesh)
        )

    def draw(self, context):
        box = self.layout.box().column()
        box.box().label(text="OOT DL Inspector")
        obj = context.object

        box.prop(obj, "ignore_render")
        box.prop(obj, "ignore_collision")

        if bpy.context.scene.f3d_type == "F3DEX3":
            box.prop(obj, "is_occlusion_planes")

            if obj.is_occlusion_planes and (not obj.ignore_render or not obj.ignore_collision):
                box.label(icon="INFO", text="Suggest Ignore Render & Ignore Collision.")

        if not (obj.parent is not None and isinstance(obj.parent.data, Armature)):
            actorScaleBox = box.box().column()
            prop_split(actorScaleBox, obj, "ootActorScale", "Actor Scale")
            actorScaleBox.label(text="This applies to actor exports only.", icon="INFO")


class MM_MaterialPanel(Panel):
    bl_label = "OOT Material"
    bl_idname = "MATERIAL_PT_MM_Material_Inspector"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return context.material is not None and context.scene.gameEditorMode == "MM"

    def draw(self, context):
        layout = self.layout
        mat = context.material
        col = layout.column()

        if (
            hasattr(context, "object")
            and context.object is not None
            and context.object.parent is not None
            and isinstance(context.object.parent.data, Armature)
        ):
            drawLayer = context.object.parent.ootDrawLayer
            if drawLayer != mat.f3d_mat.draw_layer.oot:
                col.label(text="Draw layer is being overriden by skeleton.", icon="OUTLINER_DATA_ARMATURE")
        else:
            drawLayer = mat.f3d_mat.draw_layer.oot

        dynMatProps: OOTDynamicMaterialProperty = mat.ootMaterial
        dynMatProps.draw_props(col.box().column(), mat, drawLayer)


class MM_DrawLayersPanel(Panel):
    bl_label = "Draw Layers"
    bl_idname = "WORLD_PT_MM_Draw_Layers_Panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "world"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return context.scene.gameEditorMode == "MM"

    def draw(self, context):
        world = context.scene.world
        if not world:
            return
        ootDefaultRenderModeProp: OOTDefaultRenderModesProperty = world.ootDefaultRenderModes
        ootDefaultRenderModeProp.draw_props(self.layout)


class MM_ExportDLPanel(MM_Panel):
    bl_idname = "MM_PT_dl_io"
    bl_label = "Display Lists"

    # called every frame
    def draw(self, context):
        col = self.layout.column()

        export_box = col.box()
        export_settings: Z64_DLExportSettings = context.scene.fast64.z64.DLExportSettings
        export_settings.draw_props(export_box)
        export_box.operator(OOT_ExportDL.bl_idname)

        import_box = col.box()
        import_settings: Z64_DLImportSettings = context.scene.fast64.z64.DLImportSettings
        import_settings.draw_props(import_box)
        import_box.operator(OOT_ImportDL.bl_idname)


mm_dl_writer_panel_classes = (
    MM_DisplayListPanel,
    MM_MaterialPanel,
    MM_DrawLayersPanel,
    MM_ExportDLPanel,
)


def f3d_panels_register():
    for cls in mm_dl_writer_panel_classes:
        register_class(cls)


def f3d_panels_unregister():
    for cls in mm_dl_writer_panel_classes:
        unregister_class(cls)
