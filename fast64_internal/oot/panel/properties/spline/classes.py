from bpy.types import PropertyGroup
from bpy.props import IntProperty


# draw is handled by the panel class (panel.properties.spline)
class OOTSplineProperty(PropertyGroup):
    index: IntProperty(default=0, min=0)
