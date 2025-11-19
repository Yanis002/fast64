from bpy.utils import register_class, unregister_class

from ...panels import OOT_Panel

# Note: in this context "object" means a game object


class Z64_ExportObjectPanel(OOT_Panel):
    bl_idname = "Z64_PT_export_object"
    bl_label = "Object Exporter"

    def draw(self, context):
        layout = self.layout

        # TODO: do something about flipbooks
        layout.label(text="This won't handle flipbooks.", icon="ERROR")

        context.scene.fast64.oot.object_export_settings.draw_props(layout.box().column())
        context.scene.fast64.oot.object_import_settings.draw_props(layout.box().column())


panel_classes = (Z64_ExportObjectPanel,)


def object_panels_register():
    for cls in panel_classes:
        register_class(cls)


def object_panels_unregister():
    for cls in reversed(panel_classes):
        unregister_class(cls)
