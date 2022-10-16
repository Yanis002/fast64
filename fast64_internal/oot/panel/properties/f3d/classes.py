from bpy.props import StringProperty, PointerProperty, BoolProperty, EnumProperty
from bpy.types import PropertyGroup, Object, World, Material
from bpy.utils import register_class, unregister_class
from .....f3d.f3d_parser import ootEnumDrawLayers
from ....model.classes import OOTDynamicTransformProperty


class OOTDefaultRenderModesProperty(PropertyGroup):
    expandTab: BoolProperty()
    opaqueCycle1: StringProperty(default="G_RM_AA_ZB_OPA_SURF")
    opaqueCycle2: StringProperty(default="G_RM_AA_ZB_OPA_SURF2")
    transparentCycle1: StringProperty(default="G_RM_AA_ZB_XLU_SURF")
    transparentCycle2: StringProperty(default="G_RM_AA_ZB_XLU_SURF2")
    overlayCycle1: StringProperty(default="G_RM_AA_ZB_OPA_SURF")
    overlayCycle2: StringProperty(default="G_RM_AA_ZB_OPA_SURF2")


class OOTDynamicMaterialDrawLayerProperty(PropertyGroup):
    segment8: BoolProperty()
    segment9: BoolProperty()
    segmentA: BoolProperty()
    segmentB: BoolProperty()
    segmentC: BoolProperty()
    segmentD: BoolProperty()
    customCall0: BoolProperty()
    customCall0_seg: StringProperty(description="Segment address of a display list to call, e.g. 0x08000010")
    customCall1: BoolProperty()
    customCall1_seg: StringProperty(description="Segment address of a display list to call, e.g. 0x08000010")


# The reason these are separate is for the case when the user changes the material draw layer, but not the
# dynamic material calls. This could cause crashes which would be hard to detect.
class OOTDynamicMaterialProperty(PropertyGroup):
    opaque: PointerProperty(type=OOTDynamicMaterialDrawLayerProperty)
    transparent: PointerProperty(type=OOTDynamicMaterialDrawLayerProperty)


oot_dl_writer_classes = (
    OOTDefaultRenderModesProperty,
    OOTDynamicMaterialDrawLayerProperty,
    OOTDynamicMaterialProperty,
    OOTDynamicTransformProperty,
)


def oot_dl_writer_register():
    for cls in oot_dl_writer_classes:
        register_class(cls)

    Object.ootDrawLayer = EnumProperty(items=ootEnumDrawLayers, default="Opaque")

    # Doesn't work since all static meshes are pre-transformed
    # Object.ootDynamicTransform = PointerProperty(type = OOTDynamicTransformProperty)
    World.ootDefaultRenderModes = PointerProperty(type=OOTDefaultRenderModesProperty)
    Material.ootMaterial = PointerProperty(type=OOTDynamicMaterialProperty)


def oot_dl_writer_unregister():
    for cls in reversed(oot_dl_writer_classes):
        unregister_class(cls)

    del Material.ootMaterial
