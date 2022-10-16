from bpy.types import Panel, Mesh, Armature
from bpy.utils import register_class, unregister_class
from .....utility import prop_split
from .draw import drawOOTMaterialProperty


class OOT_DisplayListPanel(Panel):
    bl_label = "Display List Inspector"
    bl_idname = "OBJECT_PT_OOT_DL_Inspector"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return context.scene.gameEditorMode == "OOT" and (
            context.object is not None and isinstance(context.object.data, Mesh)
        )

    def draw(self, context):
        box = self.layout.box()
        box.box().label(text="OOT DL Inspector")
        obj = context.object

        box.prop(obj, "ignore_render")
        box.prop(obj, "ignore_collision")

        # Doesn't work since all static meshes are pre-transformed
        # box.prop(obj.ootDynamicTransform, "billboard")


class OOT_DrawLayersPanel(Panel):
    bl_label = "OOT Draw Layers"
    bl_idname = "WORLD_PT_OOT_Draw_Layers_Panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "world"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return context.scene.gameEditorMode == "OOT"

    def draw(self, context):
        renderModes = {
            "opaqueCycle1": "Opaque Cycle 1",
            "opaqueCycle2": "Opaque Cycle 2",
            "transparentCycle1": "Transparent Cycle 1",
            "transparentCycle2": "Transparent Cycle ",
            "overlayCycle1": "Overlay Cycle 1",
            "overlayCycle2": "Overlay Cycle 2",
        }

        ootDefaultRenderModeProp = context.scene.world.ootDefaultRenderModes
        layout = self.layout
        inputGroup = layout.column()

        inputGroup.prop(
            ootDefaultRenderModeProp,
            "expandTab",
            text="Default Render Modes",
            icon="TRIA_DOWN" if ootDefaultRenderModeProp.expandTab else "TRIA_RIGHT",
        )

        if ootDefaultRenderModeProp.expandTab:
            for renderAttr in renderModes.keys():
                prop_split(inputGroup, ootDefaultRenderModeProp, renderAttr, renderModes[renderAttr])


class OOT_MaterialPanel(Panel):
    bl_label = "OOT Material"
    bl_idname = "MATERIAL_PT_OOT_Material_Inspector"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return context.material is not None and context.scene.gameEditorMode == "OOT"

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

        drawOOTMaterialProperty(col.box().column(), mat.ootMaterial, drawLayer)


oot_dl_writer_panel_classes = (
    OOT_DisplayListPanel,
    OOT_DrawLayersPanel,
    OOT_MaterialPanel,
)


def oot_dl_writer_panel_register():
    for cls in oot_dl_writer_panel_classes:
        register_class(cls)


def oot_dl_writer_panel_unregister():
    for cls in oot_dl_writer_panel_classes:
        unregister_class(cls)
