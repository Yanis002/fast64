from bpy.types import PropertyGroup
from bpy.props import IntProperty, BoolProperty, EnumProperty, StringProperty, CollectionProperty, PointerProperty
from .....data import ootRegisterQueue
from .data import ootEnumActorID, ootEnumCamTransition, ootEnumSceneSetupPreset


class OOTActorHeaderItemProperty(PropertyGroup):
    headerIndex: IntProperty(name="Scene Layer", min=4, default=4)
    expandTab: BoolProperty(name="Expand Tab")


class OOTActorHeaderProperty(PropertyGroup):
    sceneSetupPreset: EnumProperty(name="Scene Setup Preset", items=ootEnumSceneSetupPreset, default="All Scene Setups")
    childDayHeader: BoolProperty(name="Child Day Header", default=True)
    childNightHeader: BoolProperty(name="Child Night Header", default=True)
    adultDayHeader: BoolProperty(name="Adult Day Header", default=True)
    adultNightHeader: BoolProperty(name="Adult Night Header", default=True)
    cutsceneHeaders: CollectionProperty(type=OOTActorHeaderItemProperty)


class OOTActorProperty(PropertyGroup):
    actorID: EnumProperty(name="Actor", items=ootEnumActorID, default="ACTOR_PLAYER")
    actorIDCustom: StringProperty(name="Actor ID", default="ACTOR_PLAYER")
    actorParam: StringProperty(name="Actor Parameter", default="0x0000")
    rotOverride: BoolProperty(name="Override Rotation", default=False)
    rotOverrideX: StringProperty(name="Rot X", default="0")
    rotOverrideY: StringProperty(name="Rot Y", default="0")
    rotOverrideZ: StringProperty(name="Rot Z", default="0")
    headerSettings: PointerProperty(type=OOTActorHeaderProperty)


class OOTTransitionActorProperty(PropertyGroup):
    roomIndex: IntProperty(min=0)
    cameraTransitionFront: EnumProperty(items=ootEnumCamTransition, default="0x00")
    cameraTransitionFrontCustom: StringProperty(default="0x00")
    cameraTransitionBack: EnumProperty(items=ootEnumCamTransition, default="0x00")
    cameraTransitionBackCustom: StringProperty(default="0x00")

    actor: PointerProperty(type=OOTActorProperty)


class OOTEntranceProperty(PropertyGroup):
    # This is also used in entrance list, and roomIndex is obtained from the room this empty is parented to.
    spawnIndex: IntProperty(min=0)
    customActor: BoolProperty(name="Use Custom Actor")

    actor: PointerProperty(type=OOTActorProperty)


ootRegisterQueue.extend(
    [
        OOTActorHeaderItemProperty,
        OOTActorHeaderProperty,
        OOTActorProperty,
        OOTTransitionActorProperty,
        OOTEntranceProperty,
    ]
)
