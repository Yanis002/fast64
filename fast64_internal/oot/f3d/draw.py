from bpy.types import UILayout, Object
from ..f3d.classes import OOTDynamicMaterialDrawLayerProperty, OOTDynamicMaterialProperty


def drawOOTMaterialProperty(layout: UILayout, matProp: OOTDynamicMaterialProperty, drawLayer: str):
    # overlay unused?
    drawLayerSuffix = {"Opaque": "OPA", "Transparent": "XLU", "Overlay": "OVL"}

    if drawLayer != "Overlay":
        suffix = f"({drawLayerSuffix[drawLayer]})"
        layout.box().column().label(text=f"OOT Dynamic Material Properties {suffix}")
        layout.label(text="See gSPSegment calls in z_scene_table.c.")
        layout.label(text="Based off draw config index in gSceneTable.")
        drawOOTMaterialDrawLayerProperty(layout.column(), getattr(matProp, drawLayer.lower()), suffix)


def drawOOTMaterialDrawLayerProperty(
    layout: UILayout, matDrawLayerProp: OOTDynamicMaterialDrawLayerProperty, suffix: str
):
    row = layout.row()

    for colIndex in range(2):
        col = row.column()

        for rowIndex in range(3):
            i = 8 + colIndex * 3 + rowIndex
            col.prop(matDrawLayerProp, f"segment{i:X}", text=f"Segment {i:X} {suffix}")

        name = f"Custom call ({colIndex + 1}) {suffix}"
        p = f"customCall{colIndex}"
        col.prop(matDrawLayerProp, p, text=name)

        if getattr(matDrawLayerProp, p):
            col.prop(matDrawLayerProp, f"{p}_seg", text="")
