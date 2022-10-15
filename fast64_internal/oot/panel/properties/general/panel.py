from bpy.types import Panel
from bpy.utils import register_class, unregister_class
from .....utility import prop_split
from ....collision.draw import drawWaterBoxProperty
from ....oot_utility import getSceneObj, getRoomObj
from ....scene.draw import drawSceneHeaderProperty, drawAlternateSceneHeaderProperty
from ....room.draw import drawRoomHeaderProperty, drawAlternateRoomHeaderProperty
from ....cutscene.draw import drawCutsceneProperty
from ....actor.draw import drawActorProperty, drawTransitionActorProperty, drawEntranceProperty, drawActorHeaderProperty


class OOTObjectPanel(Panel):
    bl_label = "Object Inspector"
    bl_idname = "OBJECT_PT_OOT_Object_Inspector"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return context.scene.gameEditorMode == "OOT" and (context.object is not None and context.object.data is None)

    def draw(self, context):
        prop_split(self.layout, context.scene, "gameEditorMode", "Game")
        box = self.layout.box()
        box.box().label(text="OOT Object Inspector")
        obj = context.object
        objName = obj.name
        prop_split(box, obj, "ootEmptyType", "Object Type")

        sceneObj = getSceneObj(obj)
        roomObj = getRoomObj(obj)

        altSceneProp = sceneObj.ootAlternateSceneHeaders if sceneObj is not None else None
        altRoomProp = roomObj.ootAlternateRoomHeaders if roomObj is not None else None

        if obj.ootEmptyType == "Actor":
            actorProp = obj.ootActorProperty
            drawActorProperty(box, actorProp, objName)
            drawActorHeaderProperty(box.column(), actorProp.headerSettings, "Actor", altRoomProp, objName)

        elif obj.ootEmptyType == "Transition Actor":
            transLayout = box.column()
            if roomObj is None:
                transLayout.label(text="This must be part of a Room empty's hierarchy.", icon="OUTLINER")
            else:
                transActorProp = obj.ootTransitionActorProperty
                drawTransitionActorProperty(transLayout, transActorProp, roomObj.ootRoomHeader.roomIndex, objName)
                drawActorHeaderProperty(
                    transLayout, transActorProp.actor.headerSettings, "Transition Actor", altSceneProp, objName
                )

        elif obj.ootEmptyType == "Water Box":
            wBoxLayout = box.column()
            if roomObj is None:
                wBoxLayout.label(text="This must be part of a Room empty's hierarchy.", icon="OUTLINER")
            drawWaterBoxProperty(box, obj.ootWaterBoxProperty, roomObj.ootRoomHeader.roomIndex)

        elif obj.ootEmptyType == "Scene":
            menuTab = obj.ootSceneHeader.menuTab
            drawSceneHeaderProperty(box, obj.ootSceneHeader, None, None, objName)
            if menuTab == "Alternate":
                drawAlternateSceneHeaderProperty(box, obj.ootAlternateSceneHeaders, objName)
            elif menuTab == "General":
                box.box().label(text="Write Dummy Room List")
                box.label(text="Use ``NULL`` for room seg start/end offsets")
                box.prop(obj.fast64.oot.scene, "write_dummy_room_list")

        elif obj.ootEmptyType == "Room":
            drawRoomHeaderProperty(box, obj.ootRoomHeader, None, None, objName)
            if obj.ootRoomHeader.menuTab == "Alternate":
                drawAlternateRoomHeaderProperty(box, obj.ootAlternateRoomHeaders, objName)

        elif obj.ootEmptyType == "Entrance":
            entranceLayout = box.column()
            if roomObj is None:
                entranceLayout.label(text="This must be part of a Room empty's hierarchy.", icon="OUTLINER")
            else:
                split = entranceLayout.split(factor=0.5)
                split.label(text=f"Room Index: {roomObj.ootRoomHeader.roomIndex}")
                entranceProp = obj.ootEntranceProperty
                drawEntranceProperty(entranceLayout, entranceProp)
                drawActorHeaderProperty(
                    entranceLayout, entranceProp.actor.headerSettings, "Entrance", altSceneProp, objName
                )

        elif obj.ootEmptyType == "Cull Group":
            col = box.column()
            col.label(text="Use Options -> Transform -> Affect Only -> Parent ")
            col.label(text="to move object without affecting children.")

        elif obj.ootEmptyType == "LOD":
            col = box.column()
            col.box().label(text="LOD Settings (Blender Units)")
            for otherObj in obj.children:
                if context.scene.exportHiddenGeometry or not otherObj.hide_get():
                    prop_split(col, otherObj, "f3d_lod_z", otherObj.name)
            col.prop(obj, "f3d_lod_always_render_farthest")

        elif obj.ootEmptyType == "Cutscene":
            drawCutsceneProperty(box, obj)

        elif obj.ootEmptyType == "None":
            box.label(text="Geometry can be parented to this.")


oot_obj_panel_classes = (OOTObjectPanel,)


def oot_obj_panel_register():
    for cls in oot_obj_panel_classes:
        register_class(cls)


def oot_obj_panel_unregister():
    for cls in oot_obj_panel_classes:
        unregister_class(cls)
