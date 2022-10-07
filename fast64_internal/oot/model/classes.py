from bpy.types import PropertyGroup
from bpy.props import BoolProperty


class OOTDynamicTransformProperty(PropertyGroup):
    billboard: BoolProperty(name="Billboard")
