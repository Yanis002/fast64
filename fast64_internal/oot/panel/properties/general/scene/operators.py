import bpy
from bpy.types import Operator
from bpy.props import EnumProperty, IntProperty, StringProperty
from ......utility import ootGetSceneOrRoomHeader
from .....data import ootEnumSceneID
from .data import ootEnumMusicSeq


class OOT_SearchSceneEnumOperator(Operator):
    bl_idname = "object.oot_search_scene_enum_operator"
    bl_label = "Choose Scene"
    bl_property = "ootSceneID"
    bl_options = {"REGISTER", "UNDO"}

    ootSceneID: EnumProperty(items=ootEnumSceneID, default="SCENE_YDAN")

    def execute(self, context):
        context.scene.ootSceneOption = self.ootSceneID
        context.region.tag_redraw()
        self.report({"INFO"}, f"Selected: {self.ootSceneID}")
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {"RUNNING_MODAL"}


class OOT_SearchMusicSeqEnumOperator(Operator):
    bl_idname = "object.oot_search_music_seq_enum_operator"
    bl_label = "Search Music Sequence"
    bl_property = "ootMusicSeq"
    bl_options = {"REGISTER", "UNDO"}

    ootMusicSeq: EnumProperty(items=ootEnumMusicSeq, default="0x02")
    headerIndex: IntProperty(default=0, min=0)
    objName: StringProperty()

    def execute(self, context):
        sceneHeader = ootGetSceneOrRoomHeader(bpy.data.objects[self.objName], self.headerIndex, False)
        sceneHeader.musicSeq = self.ootMusicSeq
        context.region.tag_redraw()
        self.report({"INFO"}, "Selected: " + self.ootMusicSeq)
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {"RUNNING_MODAL"}
