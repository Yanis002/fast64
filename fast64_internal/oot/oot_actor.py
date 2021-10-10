
import math, os, bpy, bmesh, mathutils, xml.etree.ElementTree as ET
from collections import defaultdict
from bpy.utils import register_class, unregister_class
from io import BytesIO

from ..f3d.f3d_gbi import *
from .oot_constants import *
from .oot_utility import *

from ..utility import *


try: tree = ET.parse(os.path.dirname(os.path.abspath(__file__)) + '/ActorList.xml')
except: PluginError("ERROR: File 'fast64_internal/oot/ActorList.xml' is missing.")
root = tree.getroot()

class OOTActorDetailedProperties(bpy.types.PropertyGroup):
    pass

def editOOTActorDetailedProperties():
    global root
    paramTexts = defaultdict(list)
    datas = defaultdict(list)

    for actorNode in root:
        for elem in actorNode:
            if elem.tag == 'Parameter':
                datas[actorNode.get('ID')].append(elem.get('Params'))
                paramTexts[actorNode.get('ID')].append(elem.text)

    propAnnotations = getattr(OOTActorDetailedProperties, '__annotations__', None)
    if propAnnotations is None:
        propAnnotations = {}
        OOTActorDetailedProperties.__annotations__ = propAnnotations

    types_items = [(type, type, type) for type in datas.keys()]
    propAnnotations['type'] = bpy.props.EnumProperty(items=types_items)

    for name, values in datas.items():
        propValsIndex = name
        listPropVals = [(value, value, value) for value in values]
        valsBlEnum = bpy.props.EnumProperty(items=listPropVals)
        propAnnotations[propValsIndex] = valsBlEnum

class OOT_SearchActorIDEnumOperator(bpy.types.Operator):
    bl_idname = "object.oot_search_actor_id_enum_operator"
    bl_label = "Select Actor ID"
    bl_property = "actorID"
    bl_options = {'REGISTER', 'UNDO'}

    actorID : bpy.props.EnumProperty(items = ootEnumActorID, default = "ACTOR_PLAYER")
    actorUser : bpy.props.StringProperty(default = "Actor")
    objName : bpy.props.StringProperty()

    def execute(self, context):
        obj = bpy.data.objects[self.objName]
        if self.actorUser == "Transition Actor":
            obj.ootTransitionActorProperty.actor.actorID = self.actorID
        elif self.actorUser == "Actor":
            obj.ootActorProperty.actorID = obj.ootActorDetailedProperties.type = self.actorID
        elif self.actorUser == "Entrance":
            obj.ootEntranceProperty.actor.actorID = self.actorID
        else:
            raise PluginError("Invalid actor user for search: " + str(self.actorUser))

        bpy.context.region.tag_redraw()
        self.report({'INFO'}, "Selected: " + self.actorID)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {'RUNNING_MODAL'}

class OOTActorHeaderItemProperty(bpy.types.PropertyGroup):
    headerIndex : bpy.props.IntProperty(name = "Scene Setup", min = 4, default = 4)
    expandTab : bpy.props.BoolProperty(name = "Expand Tab")

class OOTActorHeaderProperty(bpy.types.PropertyGroup):
    sceneSetupPreset : bpy.props.EnumProperty(name = "Scene Setup Preset", items = ootEnumSceneSetupPreset, default = "All Scene Setups")
    childDayHeader : bpy.props.BoolProperty(name = "Child Day Header", default = True)
    childNightHeader : bpy.props.BoolProperty(name = "Child Night Header", default = True)
    adultDayHeader : bpy.props.BoolProperty(name = "Adult Day Header", default = True)
    adultNightHeader : bpy.props.BoolProperty(name = "Adult Night Header", default = True)
    cutsceneHeaders : bpy.props.CollectionProperty(type = OOTActorHeaderItemProperty)

def drawActorHeaderProperty(layout, headerProp, propUser, altProp, objName):
    headerSetup = layout.column()
    #headerSetup.box().label(text = "Alternate Headers")
    prop_split(headerSetup, headerProp, "sceneSetupPreset", "Scene Setup Preset")
    if headerProp.sceneSetupPreset == "Custom":
        headerSetupBox = headerSetup.column()
        headerSetupBox.prop(headerProp, 'childDayHeader', text = "Child Day")
        childNightRow = headerSetupBox.row()
        childNightRow.prop(headerProp, 'childNightHeader', text = "Child Night")
        adultDayRow = headerSetupBox.row()
        adultDayRow.prop(headerProp, 'adultDayHeader', text = "Adult Day")
        adultNightRow = headerSetupBox.row()
        adultNightRow.prop(headerProp, 'adultNightHeader', text = "Adult Night")

        childNightRow.enabled = not altProp.childNightHeader.usePreviousHeader if altProp is not None else True
        adultDayRow.enabled = not altProp.adultDayHeader.usePreviousHeader if altProp is not None else True
        adultNightRow.enabled = not altProp.adultNightHeader.usePreviousHeader if altProp is not None else True

        for i in range(len(headerProp.cutsceneHeaders)):
            drawActorHeaderItemProperty(headerSetup, propUser, headerProp.cutsceneHeaders[i], i, altProp, objName)
        drawAddButton(headerSetup, len(headerProp.cutsceneHeaders), propUser, None, objName)

def drawActorHeaderItemProperty(layout, propUser, headerItemProp, index, altProp, objName):
    box = layout.box()
    box.prop(headerItemProp, 'expandTab', text = 'Header ' + \
        str(headerItemProp.headerIndex), icon = 'TRIA_DOWN' if headerItemProp.expandTab else \
        'TRIA_RIGHT')
    
    if headerItemProp.expandTab:
        drawCollectionOps(box, index, propUser, None, objName)
        prop_split(box, headerItemProp, 'headerIndex', 'Header Index')
        if altProp is not None and headerItemProp.headerIndex >= len(altProp.cutsceneHeaders) + 4:
            box.label(text = "Header does not exist.", icon = "ERROR")
        
class OOTActorProperty(bpy.types.PropertyGroup):
    actorID : bpy.props.EnumProperty(name = 'Actor', items = ootEnumActorID, default = 'ACTOR_PLAYER')
    actorIDCustom : bpy.props.StringProperty(name = 'Actor ID', default = 'ACTOR_PLAYER')
    actorParam : bpy.props.StringProperty(name = 'Actor Parameter', default = '0x0000')
    rotOverride : bpy.props.BoolProperty(name = 'Override Rotation', default = False)
    rotOverrideX : bpy.props.StringProperty(name = 'Rot X', default = '0')
    rotOverrideY : bpy.props.StringProperty(name = 'Rot Y', default = '0')
    rotOverrideZ : bpy.props.StringProperty(name = 'Rot Z', default = '0')
    headerSettings : bpy.props.PointerProperty(type = OOTActorHeaderProperty)

paramList = []
paramList.append("")        

class OOT_SearchChestContentEnumOperator(bpy.types.Operator):
    bl_idname = "object.oot_search_chest_content_enum_operator"
    bl_label = "Select Chest Content"
    bl_property = "itemChest"
    bl_options = {'REGISTER', 'UNDO'}

    itemChest : bpy.props.EnumProperty(items = ootEnBoxContent, default = '0x48')
    objName : bpy.props.StringProperty()

    def execute(self, context):
        if self.objName in bpy.data.objects:
            bpy.data.objects[self.objName].ootActorDetailedProperties.itemChest = self.itemChest

        bpy.context.region.tag_redraw()
        self.report({'INFO'}, "Selected: " + self.itemChest)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {'RUNNING_MODAL'}

def drawActorProperty(layout, actorProp, altRoomProp, objName, detailedProp):
    #prop_split(layout, actorProp, 'actorID', 'Actor')
    actorIDBox = layout.column()
    #actorIDBox.box().label(text = "Settings")
    searchOp = actorIDBox.operator(OOT_SearchActorIDEnumOperator.bl_idname, icon = 'VIEWZOOM')
    searchOp.actorUser = "Actor"
    searchOp.objName = objName

    split = actorIDBox.split(factor = 0.5)
    split.label(text = "Actor ID")
    split.label(text = getEnumName(ootEnumActorID, actorProp.actorID))

    if actorProp.actorID == 'Custom':
        #actorIDBox.prop(actorProp, 'actorIDCustom', text = 'Actor ID')
        prop_split(actorIDBox, actorProp, 'actorIDCustom', '')
    # global root
    # for actorNode in root:
    #     if actorProp.actorID == actorNode.get('ID') == detailedProp.type:
    #         prop_split(actorIDBox, detailedProp, detailedProp.type, 'Type')

    prop_split(actorIDBox, detailedProp, detailedProp.type, 'Type')

    # for actorNode in root:
    #     for elem in actorNode:
    #         if elem.tag == 'Parameter' and actorNode.get('ID') == actorProp.actorID and elem.text == paramList[0][1]:
    #             prop_split(actorIDBox, detailedProp, 'actorProperties', 'Parameter')

    #         if actorNode.get('ID') == actorProp.actorID and elem.tag == 'Item':
    #             searchOp = actorIDBox.operator(OOT_SearchChestContentEnumOperator.bl_idname, icon='VIEWZOOM')
    #             split = actorIDBox.split(factor=0.5)
    #             split.label(text="Chest Content")
    #             split.label(text=getEnumName(ootEnBoxContent, detailedProp.itemChest))

    #         if elem.tag == 'Flag':
    #             if actorNode.get('ID') == actorProp.actorID and elem.get('Type') == 'Switch': 
    #                 prop_split(actorIDBox, detailedProp, 'switchFlag', 'Switch Flag')

    #             if actorNode.get('ID') == actorProp.actorID and elem.get('Type') == 'Chest': 
    #                 prop_split(actorIDBox, detailedProp, 'chestFlag', 'Chest Flag')

    #             if actorNode.get('ID') == actorProp.actorID and elem.get('Type') == 'Collectible': 
    #                 prop_split(actorIDBox, detailedProp, 'itemDropFlag', 'Collectible Flag')

    #         if actorNode.get('ID') == actorProp.actorID and elem.tag == 'Collectible':
    #             prop_split(actorIDBox, detailedProp, 'itemDrop', 'Collectible Drop')

    #layout.box().label(text = 'Actor IDs defined in include/z64actors.h.')
    prop_split(actorIDBox, actorProp, "actorParam", 'Actor Parameter')
    
    actorIDBox.prop(actorProp, 'rotOverride', text = 'Override Rotation (ignore Blender rot)')
    if actorProp.rotOverride:
        prop_split(actorIDBox, actorProp, 'rotOverrideX', 'Rot X')
        prop_split(actorIDBox, actorProp, 'rotOverrideY', 'Rot Y')
        prop_split(actorIDBox, actorProp, 'rotOverrideZ', 'Rot Z')

    drawActorHeaderProperty(actorIDBox, actorProp.headerSettings, "Actor", altRoomProp, objName)

# print(OOTActorDetailedProperties_annotations)
    # global root
    # global paramList

    # actorID = "ACTOR_EN_TEST"

    # for actorNode in root:
    #     for elem in actorNode:
    #         propType = elem.get('Type')
    #         if propType is not None:
    #             if elem.tag == 'Flag':
    #                 if propType == 'Switch': switchFlag: bpy.props.StringProperty(name = 'Switch Flag', default = '0x0000')
    #                 if propType == 'Chest': chestFlag: bpy.props.StringProperty(name = 'Chest Flag', default = '0x0000')
    #                 if propType == 'Collectible': itemDropFlag: bpy.props.StringProperty(name = 'Collectible Flag', default = '0x0000')

    #             if elem.tag == 'Collectible': itemDrop: bpy.props.StringProperty(name = 'Collectible Drop', default = '0x0000')
    #             if elem.tag == 'Item': itemChest: bpy.props.EnumProperty(name = 'Chest Content', items = ootEnBoxContent, default = '0x48')

    #         if elem.tag == 'Parameter' and actorNode.get('ID') == actorID:
    #             if paramList[0] != "" and paramList[len(paramList) - 1] != elem.get('Params') and elem.get('Params') is not None:
    #                 paramList.append((f"{elem.get('Params')}", f"{elem.text}", ""))
    #             else:
    #                 paramList[0] = ((f"{elem.get('Params')}", f"{elem.text}", ""))

    #         if elem.tag == 'Parameter' and elem.get('Params') is not None:
    #             actorProperties: bpy.props.EnumProperty(name = 'Parameters', items = paramList)

class OOTTransitionActorProperty(bpy.types.PropertyGroup):
    roomIndex : bpy.props.IntProperty(min = 0)
    cameraTransitionFront : bpy.props.EnumProperty(items = ootEnumCamTransition, default = '0x00')
    cameraTransitionFrontCustom : bpy.props.StringProperty(default = '0x00')
    cameraTransitionBack : bpy.props.EnumProperty(items = ootEnumCamTransition, default = '0x00')
    cameraTransitionBackCustom : bpy.props.StringProperty(default = '0x00')
    
    actor : bpy.props.PointerProperty(type = OOTActorProperty)

def drawTransitionActorProperty(layout, transActorProp, altSceneProp, roomObj, objName):
    actorIDBox = layout.column()
    #actorIDBox.box().label(text = "Properties")
    #prop_split(actorIDBox, transActorProp, 'actorID', 'Actor')
    #actorIDBox.box().label(text = "Actor ID: " + getEnumName(ootEnumActorID, transActorProp.actor.actorID))
    searchOp = actorIDBox.operator(OOT_SearchActorIDEnumOperator.bl_idname, icon = 'VIEWZOOM')
    searchOp.actorUser = "Transition Actor"
    searchOp.objName = objName

    split = actorIDBox.split(factor = 0.5)
    split.label(text = "Actor ID")
    split.label(text = getEnumName(ootEnumActorID, transActorProp.actor.actorID))

    if transActorProp.actor.actorID == 'Custom':
        prop_split(actorIDBox, transActorProp.actor, 'actorIDCustom', '')

    #layout.box().label(text = 'Actor IDs defined in include/z64actors.h.')
    prop_split(actorIDBox, transActorProp.actor, "actorParam", 'Actor Parameter')

    if roomObj is None:
        actorIDBox.label(text = "This must be part of a Room empty's hierarchy.", icon = "ERROR")
    else:
        label_split(actorIDBox, "Room To Transition From", str(roomObj.ootRoomHeader.roomIndex))
    prop_split(actorIDBox, transActorProp, "roomIndex", "Room To Transition To")
    actorIDBox.label(text = "Y+ side of door faces toward the \"from\" room.", icon = "ERROR")
    drawEnumWithCustom(actorIDBox, transActorProp, "cameraTransitionFront", "Camera Transition Front", "")
    drawEnumWithCustom(actorIDBox, transActorProp, "cameraTransitionBack", "Camera Transition Back", "")

    drawActorHeaderProperty(actorIDBox, transActorProp.actor.headerSettings, "Transition Actor", altSceneProp, objName)
    
class OOTEntranceProperty(bpy.types.PropertyGroup):
    # This is also used in entrance list, and roomIndex is obtained from the room this empty is parented to.
    spawnIndex : bpy.props.IntProperty(min = 0)
    customActor : bpy.props.BoolProperty(name = "Use Custom Actor")
    actor : bpy.props.PointerProperty(type = OOTActorProperty)

def drawEntranceProperty(layout, obj, altSceneProp, objName):
    box = layout.column()
    #box.box().label(text = "Properties")
    roomObj = getRoomObj(obj)
    if roomObj is not None:
        split = box.split(factor = 0.5)
        split.label(text = "Room Index")
        split.label(text = str(roomObj.ootRoomHeader.roomIndex))
    else:
        box.label(text = "This must be part of a Room empty's hierarchy.", icon = "ERROR")

    entranceProp = obj.ootEntranceProperty
    prop_split(box, entranceProp, "spawnIndex", "Spawn Index")
    prop_split(box, entranceProp.actor, "actorParam", "Actor Param")
    box.prop(entranceProp, "customActor")
    if entranceProp.customActor:
        prop_split(box, entranceProp.actor, "actorIDCustom", "Actor ID Custom")
    
    drawActorHeaderProperty(box, entranceProp.actor.headerSettings, "Entrance", altSceneProp, objName)
