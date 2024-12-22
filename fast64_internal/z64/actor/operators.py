import bpy
from bpy.types import Operator
from bpy.props import EnumProperty, StringProperty
from bpy.utils import register_class, unregister_class
from ...utility import PluginError
from ..constants import oot_data, mm_data


class OOT_SearchActorIDEnumOperator(Operator):
    bl_idname = "object.oot_search_actor_id_enum_operator"
    bl_label = "Select Actor ID"
    bl_property = "actorID"
    bl_options = {"REGISTER", "UNDO"}

    actorID: EnumProperty(items=oot_data.actorData.ootEnumActorID, default="ACTOR_PLAYER")
    actorUser: StringProperty(default="Actor")
    objName: StringProperty()

    def execute(self, context):
        obj = bpy.data.objects[self.objName]
        if self.actorUser == "Transition Actor":
            obj.ootTransitionActorProperty.actor.actorID = self.actorID
        elif self.actorUser == "Actor":
            obj.ootActorProperty.actorID = self.actorID
        elif self.actorUser == "Entrance":
            obj.ootEntranceProperty.actor.actorID = self.actorID
        else:
            raise PluginError("Invalid actor user for search: " + str(self.actorUser))

        context.region.tag_redraw()
        self.report({"INFO"}, "Selected: " + self.actorID)
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
            obj.mm_transition_actor_property.actor.actorID = self.actorID
        elif self.actorUser == "Actor":
            obj.mm_actor_property.actorID = self.actorID
        elif self.actorUser == "Entrance":
            obj.ootEntrmm_entrance_propertyanceProperty.actor.actorID = self.actorID
        else:
            raise PluginError("Invalid actor user for search: " + str(self.actorUser))

        context.region.tag_redraw()
        self.report({"INFO"}, "Selected: " + self.actorID)
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {"RUNNING_MODAL"}


classes = (
    OOT_SearchActorIDEnumOperator,
    MM_SearchActorIDEnumOperator,
)


def actor_ops_register():
    for cls in classes:
        register_class(cls)


def actor_ops_unregister():
    for cls in reversed(classes):
        unregister_class(cls)