from bpy.types import Operator
from bpy.props import IntProperty, StringProperty
from bpy.utils import register_class, unregister_class
from .utility import getCollection


class OOTCollectionAdd(Operator):
    bl_idname = "object.oot_collection_add"
    bl_label = "Add Item"
    bl_options = {"REGISTER", "UNDO"}

    option: IntProperty()
    collectionType: StringProperty(default="Actor")
    subIndex: IntProperty(default=0)
    objName: StringProperty()

    def execute(self, context):
        collection = getCollection(self.objName, self.collectionType, self.subIndex)

        collection.add()
        collection.move(len(collection) - 1, self.option)
        return {"FINISHED"}


class OOTCollectionRemove(Operator):
    bl_idname = "object.oot_collection_remove"
    bl_label = "Remove Item"
    bl_options = {"REGISTER", "UNDO"}

    option: IntProperty()
    collectionType: StringProperty(default="Actor")
    subIndex: IntProperty(default=0)
    objName: StringProperty()

    def execute(self, context):
        collection = getCollection(self.objName, self.collectionType, self.subIndex)
        collection.remove(self.option)
        return {"FINISHED"}


class OOTCollectionMove(Operator):
    bl_idname = "object.oot_collection_move"
    bl_label = "Move Item"
    bl_options = {"REGISTER", "UNDO"}

    option: IntProperty()
    offset: IntProperty()
    subIndex: IntProperty(default=0)
    objName: StringProperty()

    collectionType: StringProperty(default="Actor")

    def execute(self, context):
        collection = getCollection(self.objName, self.collectionType, self.subIndex)
        collection.move(self.option, self.option + self.offset)
        return {"FINISHED"}


oot_utility_classes = (
    OOTCollectionAdd,
    OOTCollectionRemove,
    OOTCollectionMove,
)


def oot_utility_register():
    for cls in oot_utility_classes:
        register_class(cls)


def oot_utility_unregister():
    for cls in reversed(oot_utility_classes):
        unregister_class(cls)
