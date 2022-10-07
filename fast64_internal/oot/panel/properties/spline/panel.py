from bpy.types import Panel, Curve, Object
from bpy.utils import register_class, unregister_class
from bpy.props import PointerProperty
from .....utility import prop_split
from ....spline.classes import OOTSplineProperty


class OOTSplinePanel(Panel):
    bl_label = "Spline Inspector"
    bl_idname = "OBJECT_PT_OOT_Spline_Inspector"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return context.scene.gameEditorMode == "OOT" and (
            context.object is not None and type(context.object.data) == Curve
        )

    def draw(self, context):
        box = self.layout.box()
        box.box().label(text="OOT Spline Inspector")
        curve = context.object.data

        if curve.splines[0].type != "NURBS":
            box.label(text="Only NURBS curves are compatible.")
        else:
            prop_split(box, context.object.ootSplineProperty, "index", "Index")


oot_spline_classes = (OOTSplineProperty,)

def oot_spline_register():
    for cls in oot_spline_classes:
        register_class(cls)

    Object.ootSplineProperty = PointerProperty(type=OOTSplineProperty)


def oot_spline_unregister():

    for cls in reversed(oot_spline_classes):
        unregister_class(cls)

    del Object.ootSplineProperty


oot_spline_panel_classes = (OOTSplinePanel,)

def oot_spline_panel_register():
    for cls in oot_spline_panel_classes:
        register_class(cls)


def oot_spline_panel_unregister():
    for cls in oot_spline_panel_classes:
        unregister_class(cls)
