import bpy
from bpy.types import Operator
from bpy.props import EnumProperty, StringProperty
from ......utility import PluginError
from .....data import ootRegisterQueue
from .data import ootEnumActorID


class OOT_SearchActorIDEnumOperator(Operator):
    bl_idname = "object.oot_search_actor_id_enum_operator"
    bl_label = "Select Actor ID"
    bl_property = "actorID"
    bl_options = {"REGISTER", "UNDO"}

    actorID: EnumProperty(items=ootEnumActorID, default="ACTOR_PLAYER")
    actorUser: StringProperty(default="Actor")
    objName: StringProperty()

    def execute(self, context):
        obj = bpy.data.objects[self.objName]

        match self.actorUser:
            case "Transition Actor":
                obj.ootTransitionActorProperty.actor.actorID = self.actorID
            case "Actor":
                obj.ootActorProperty.actorID = self.actorID
            case "Entrance":
                obj.ootEntranceProperty.actor.actorID = self.actorID
            case _:
                raise PluginError(f"Invalid actor user for search: {self.actorUser}")

        context.region.tag_redraw()
        self.report({"INFO"}, f"Selected: {self.actorID}")
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {"RUNNING_MODAL"}


ootRegisterQueue.append(OOT_SearchActorIDEnumOperator)
