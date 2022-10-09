from bpy.types import Panel, Camera, Object
from bpy.utils import register_class, unregister_class
from ....collision.draw import drawCollisionProperty, drawCameraProperty


class OOT_CameraPosPanel(Panel):
    bl_label = "Camera Position Inspector"
    bl_idname = "OBJECT_PT_OOT_Camera_Position_Inspector"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return context.scene.gameEditorMode == "OOT" and isinstance(context.object.data, Camera)

    def draw(self, context):
        obj: Object = context.object
        drawCameraProperty(self.layout.box(), obj.ootCameraPositionProperty, obj.data)


class OOT_CollisionPanel(Panel):
    bl_label = "Collision Inspector"
    bl_idname = "MATERIAL_PT_OOT_Collision_Inspector"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return context.scene.gameEditorMode == "OOT" and context.material is not None

    def draw(self, context):
        box = self.layout.box().column()
        collisionProp = context.material.ootCollisionProperty

        box.prop(
            collisionProp,
            "expandTab",
            text="OOT Collision Properties",
            icon="TRIA_DOWN" if collisionProp.expandTab else "TRIA_RIGHT",
        )

        if collisionProp.expandTab:
            drawCollisionProperty(box, collisionProp)


oot_col_panel_classes = (
    OOT_CollisionPanel,
    OOT_CameraPosPanel,
)

def oot_col_panel_register():
    for cls in oot_col_panel_classes:
        register_class(cls)


def oot_col_panel_unregister():
    for cls in oot_col_panel_classes:
        unregister_class(cls)
