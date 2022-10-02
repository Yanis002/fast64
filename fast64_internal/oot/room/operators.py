import bpy
from bpy.types import Operator
from bpy.props import EnumProperty, IntProperty, StringProperty
from ...utility import ootGetSceneOrRoomHeader
from ..oot_constants import ootEnumObjectID


class OOT_SearchObjectEnumOperator(Operator):
    bl_idname = "object.oot_search_object_enum_operator"
    bl_label = "Search Object ID"
    bl_property = "ootObjectID"
    bl_options = {"REGISTER", "UNDO"}

    ootObjectID: EnumProperty(items=ootEnumObjectID, default="OBJECT_HUMAN")
    headerIndex: IntProperty(default=0, min=0)
    index: IntProperty(default=0, min=0)
    objName: StringProperty()

    def execute(self, context):
        roomHeader = ootGetSceneOrRoomHeader(bpy.data.objects[self.objName], self.headerIndex, True)
        roomHeader.objectList[self.index].objectID = self.ootObjectID
        context.region.tag_redraw()
        self.report({"INFO"}, "Selected: " + self.ootObjectID)
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {"RUNNING_MODAL"}
