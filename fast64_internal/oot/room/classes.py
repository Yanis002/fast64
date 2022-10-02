from bpy.types import PropertyGroup

from bpy.props import (
    PointerProperty,
    EnumProperty,
    BoolProperty,
    StringProperty,
    CollectionProperty,
    IntProperty,
    FloatProperty,
    FloatVectorProperty,
)

from ..oot_constants import (
    ootRegisterQueue,
    ootEnumHeaderMenu,
    ootEnumLinkIdle,
    ootEnumObjectID,
    ootEnumRoomShapeType,
    ootEnumRoomMenu,
    ootEnumRoomMenuAlternate,
    ootEnumRoomBehaviour,
)


class OOTObjectProperty(PropertyGroup):
    expandTab: BoolProperty(name="Expand Tab")
    objectID: EnumProperty(items=ootEnumObjectID, default="OBJECT_HUMAN")
    objectIDCustom: StringProperty(default="OBJECT_HUMAN")


class OOTRoomHeaderProperty(PropertyGroup):
    expandTab: BoolProperty(name="Expand Tab")
    menuTab: EnumProperty(items=ootEnumRoomMenu)
    altMenuTab: EnumProperty(items=ootEnumRoomMenuAlternate)
    usePreviousHeader: BoolProperty(name="Use Previous Header", default=True)

    roomIndex: IntProperty(name="Room Index", default=0, min=0)
    roomBehaviour: EnumProperty(items=ootEnumRoomBehaviour, default="0x00")
    roomBehaviourCustom: StringProperty(default="0x00")
    disableWarpSongs: BoolProperty(name="Disable Warp Songs")
    showInvisibleActors: BoolProperty(name="Show Invisible Actors")
    linkIdleMode: EnumProperty(name="Link Idle Mode", items=ootEnumLinkIdle, default="0x00")
    linkIdleModeCustom: StringProperty(name="Link Idle Mode Custom", default="0x00")

    useCustomBehaviourX: BoolProperty(name="Use Custom Behaviour X")
    useCustomBehaviourY: BoolProperty(name="Use Custom Behaviour Y")

    customBehaviourX: StringProperty(name="Custom Behaviour X", default="0x00")

    customBehaviourY: StringProperty(name="Custom Behaviour Y", default="0x00")

    setWind: BoolProperty(name="Set Wind")
    windVector: FloatVectorProperty(name="Wind Vector", size=3)

    leaveTimeUnchanged: BoolProperty(name="Leave Time Unchanged", default=True)
    timeHours: IntProperty(name="Hours", default=0, min=0, max=23)  # 0xFFFE
    timeMinutes: IntProperty(name="Minutes", default=0, min=0, max=59)
    timeSpeed: FloatProperty(name="Time Speed", default=1, min=-13, max=13)  # 0xA

    disableSkybox: BoolProperty(name="Disable Skybox")
    disableSunMoon: BoolProperty(name="Disable Sun/Moon")

    echo: StringProperty(name="Echo", default="0x00")

    objectList: CollectionProperty(type=OOTObjectProperty)

    roomShape: EnumProperty(items=ootEnumRoomShapeType, default="ROOM_SHAPE_TYPE_NORMAL")
    defaultCullDistance: IntProperty(name="Default Cull Distance", min=1, default=100)


class OOTAlternateRoomHeaderProperty(PropertyGroup):
    childNightHeader: PointerProperty(name="Child Night Header", type=OOTRoomHeaderProperty)
    adultDayHeader: PointerProperty(name="Adult Day Header", type=OOTRoomHeaderProperty)
    adultNightHeader: PointerProperty(name="Adult Night Header", type=OOTRoomHeaderProperty)
    cutsceneHeaders: CollectionProperty(type=OOTRoomHeaderProperty)

    headerMenuTab: EnumProperty(name="Header Menu", items=ootEnumHeaderMenu)
    currentCutsceneIndex: IntProperty(min=4, default=4)


ootRegisterQueue.extend(
    [
        OOTObjectProperty,
        OOTRoomHeaderProperty,
        OOTAlternateRoomHeaderProperty,
    ]
)
