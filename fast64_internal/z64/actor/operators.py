import bpy
from bpy.types import Operator
from bpy.props import EnumProperty, StringProperty
from bpy.utils import register_class, unregister_class
from ...utility import PluginError
from ..constants import oot_data, mm_data


class OOT_SearchChestContentEnumOperator(Operator):
    bl_idname = "object.oot_search_chest_content_enum_operator"
    bl_label = "Select Chest Content"
    bl_property = "chest_content"
    bl_options = {"REGISTER", "UNDO"}

    chest_content: EnumProperty(items=oot_data.actorData.ootEnumChestContent, default="item_heart")
    obj_name: StringProperty()
    prop_name: StringProperty()

    def execute(self, context):
        setattr(bpy.data.objects[self.obj_name].ootActorProperty, self.prop_name, self.chest_content)
        context.region.tag_redraw()
        self.report({"INFO"}, f"Selected: {self.chest_content}")
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {"RUNNING_MODAL"}


class MM_SearchActorIDEnumOperator(Operator):
    bl_idname = "object.mm_search_actor_id_enum_operator"
    bl_label = "Select Actor ID"
    bl_property = "actorID"
    bl_options = {"REGISTER", "UNDO"}

    actorID: EnumProperty(items=mm_data.actor_data.enum_actor_id, default="ACTOR_PLAYER")
    actorUser: StringProperty(default="Actor")
    objName: StringProperty()

    def execute(self, context):
        obj = bpy.data.objects[self.objName]
        if self.actorUser == "Transition Actor":
            obj.ootTransitionActorProperty.actor.mm_actor_id = self.actorID
        elif self.actorUser == "Actor":
            obj.ootActorProperty.mm_actor_id = self.actorID
        elif self.actorUser == "Entrance":
            obj.ootEntranceProperty.actor.mm_actor_id = self.actorID
        else:
            raise PluginError("Invalid actor user for search: " + str(self.actorUser))

        context.region.tag_redraw()
        self.report({"INFO"}, "Selected: " + self.actorID)


class OOT_SearchNaviMsgIDEnumOperator(Operator):
    bl_idname = "object.oot_search_navi_msg_id_enum_operator"
    bl_label = "Select Message ID"
    bl_property = "navi_msg_id"
    bl_options = {"REGISTER", "UNDO"}

    navi_msg_id: EnumProperty(items=oot_data.actorData.ootEnumNaviMessageData, default="msg_00")
    obj_name: StringProperty()
    prop_name: StringProperty()

    def execute(self, context):
        setattr(bpy.data.objects[self.obj_name].ootActorProperty, self.prop_name, self.navi_msg_id)
        context.region.tag_redraw()
        self.report({"INFO"}, f"Selected: {self.navi_msg_id}")
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {"RUNNING_MODAL"}


class OOT_SearchActorIDEnumOperator(Operator):
    bl_idname = "object.oot_search_actor_id_enum_operator"
    bl_label = "Select Actor ID"
    bl_property = "actor_id"
    bl_options = {"REGISTER", "UNDO"}

    actor_id: EnumProperty(items=lambda self, context: oot_data.actorData.getItems(self.actor_user))
    actor_user: StringProperty(default="Actor")
    obj_name: StringProperty()

    actorID: EnumProperty(items=oot_data.actorData.ootEnumActorID, default="ACTOR_PLAYER")
    actorUser: StringProperty(default="Actor")
    objName: StringProperty()

    def execute(self, context):
        obj = bpy.data.objects[self.obj_name]

        if self.actor_user == "Transition Actor":
            obj.ootTransitionActorProperty.actor.actor_id = self.actor_id
        elif self.actor_user == "Actor":
            obj.ootActorProperty.actor_id = self.actor_id
        else:
            raise PluginError("Invalid actor user for search: " + str(self.actor_user))

        context.region.tag_redraw()
        self.report({"INFO"}, f"Selected: {self.actor_id}")
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {"RUNNING_MODAL"}


classes = (
    MM_SearchActorIDEnumOperator,
    OOT_SearchActorIDEnumOperator,
    OOT_SearchChestContentEnumOperator,
    OOT_SearchNaviMsgIDEnumOperator,
)


def actor_ops_register():
    for cls in classes:
        register_class(cls)


def actor_ops_unregister():
    for cls in reversed(classes):
        unregister_class(cls)
