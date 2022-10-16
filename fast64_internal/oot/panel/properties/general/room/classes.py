from bpy.types import PropertyGroup
from .....data import ootRegisterQueue, ootEnumHeaderMenu

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

from .data import (
    ootEnumRoomShapeType,
    ootEnumRoomMenu,
    ootEnumRoomMenuAlternate,
    ootEnumLinkIdle,
    ootEnumObjectID,
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
    roomIsHot: BoolProperty(
        name="Use Room Heat Behavior",
        description="Use heat timer/screen effect, overrides Link Idle Mode",
        default=False,
    )

    useCustomBehaviourX: BoolProperty(name="Use Custom Behaviour X")  # unused
    useCustomBehaviourY: BoolProperty(name="Use Custom Behaviour Y")  # unused

    customBehaviourX: StringProperty(name="Custom Behaviour X", default="0x00")

    customBehaviourY: StringProperty(name="Custom Behaviour Y", default="0x00")

    setWind: BoolProperty(name="Set Wind")
    windVector: FloatVectorProperty(name="Wind Vector", size=3)

    leaveTimeUnchanged: BoolProperty(name="Leave Time Unchanged", default=True)
    timeHours: IntProperty(name="Hours", default=0, min=0, max=23)  # 0xFFFE
    timeMinutes: IntProperty(name="Minutes", default=0, min=0, max=59)

    # the time speed variable in OoT is an unsigned byte,
    # thus it can't have negative values or float-like values
    # if the value if 255 (0xFF) the game force the speed to be 0
    timeSpeed: FloatProperty(
        name="Time Speed",
        description="0: Frozen, 1: Normal, 2: Twice as fast, etc...",
        default=1,
        min=0,
        max=25.5,
        precision=1,
    )

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
