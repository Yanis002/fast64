from bpy.utils import register_class, unregister_class
from ...panel import OOT_Panel
from .operators import toolOpsToRegister


class OoT_ToolsPanel(OOT_Panel):
    bl_idname = "OOT_PT_operators"
    bl_label = "OOT Tools"

    def draw(self, context):
        for toolOp in toolOpsToRegister:
            self.layout.column().operator(toolOp.bl_idname)


oot_operator_panel_classes = [
    OoT_ToolsPanel,
]

def oot_operator_panel_register():
    for cls in oot_operator_panel_classes:
        register_class(cls)


def oot_operator_panel_unregister():
    for cls in oot_operator_panel_classes:
        unregister_class(cls)


def oot_operator_register():
    for cls in toolOpsToRegister:
        register_class(cls)


def oot_operator_unregister():
    for cls in reversed(toolOpsToRegister):
        unregister_class(cls)
