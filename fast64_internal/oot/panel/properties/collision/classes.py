from math import pi
from bpy.types import PropertyGroup, Camera, Object, Material
from bpy.utils import register_class, unregister_class
from bpy.props import IntProperty, StringProperty, EnumProperty, BoolProperty, PointerProperty, FloatProperty

from .data import (
    ootEnumFloorSetting,
    ootEnumWallSetting,
    ootEnumFloorProperty,
    ootEnumConveyer,
    ootEnumConveyorSpeed,
    ootEnumCollisionTerrain,
    ootEnumCollisionSound,
    ootEnumCameraSType,
)


class OOTCameraPositionProperty(PropertyGroup):
    index: IntProperty(min=0)
    jfifID: StringProperty(default="-1")
    camSType: EnumProperty(items=ootEnumCameraSType, default="CAM_SET_NONE")
    camSTypeCustom: StringProperty(default="CAM_SET_NONE")
    hasPositionData: BoolProperty(default=True, name="Has Position Data")


class OOTCameraPositionPropertyRef(PropertyGroup):
    camera: PointerProperty(type=Camera)


class OOTMaterialCollisionProperty(PropertyGroup):
    expandTab: BoolProperty()

    ignoreCameraCollision: BoolProperty()
    ignoreActorCollision: BoolProperty()
    ignoreProjectileCollision: BoolProperty()

    eponaBlock: BoolProperty()
    decreaseHeight: BoolProperty()
    floorSettingCustom: StringProperty(default="0x00")
    floorSetting: EnumProperty(items=ootEnumFloorSetting, default="0x00")
    wallSettingCustom: StringProperty(default="0x00")
    wallSetting: EnumProperty(items=ootEnumWallSetting, default="0x00")
    floorPropertyCustom: StringProperty(default="0x00")
    floorProperty: EnumProperty(items=ootEnumFloorProperty, default="0x00")
    exitID: IntProperty(default=0, min=0)
    cameraID: IntProperty(default=0, min=0)
    isWallDamage: BoolProperty()
    conveyorOption: EnumProperty(items=ootEnumConveyer)
    conveyorRotation: FloatProperty(min=0, max=2 * pi, subtype="ANGLE")
    conveyorSpeed: EnumProperty(items=ootEnumConveyorSpeed, default="0x00")
    conveyorSpeedCustom: StringProperty(default="0x00")
    conveyorKeepMomentum: BoolProperty()
    hookshotable: BoolProperty()
    echo: StringProperty(default="0x00")
    lightingSetting: IntProperty(default=0, min=0)
    terrainCustom: StringProperty(default="0x00")
    terrain: EnumProperty(items=ootEnumCollisionTerrain, default="0x00")
    soundCustom: StringProperty(default="0x00")
    sound: EnumProperty(items=ootEnumCollisionSound, default="0x00")


class OOTWaterBoxProperty(PropertyGroup):
    # maximums enforced by the game, see macros inside ``z64bgcheck.h``
    lighting: IntProperty(name="Lighting", min=0, max=31)
    camera: IntProperty(name="Camera", min=0, max=255)

    # sets whether the waterbox supposed to be global to a scene
    # uses 0x3F as room index if ``True``
    isGlobal: BoolProperty(
        name="Is Global to Scene",
        description="This will keep the WaterBox loaded all the time.",
        default=False,
    )


oot_col_classes = (
    OOTWaterBoxProperty,
    OOTCameraPositionPropertyRef,
    OOTCameraPositionProperty,
    OOTMaterialCollisionProperty,
)


def oot_col_register():
    for cls in oot_col_classes:
        register_class(cls)

    # Collision
    Object.ootCameraPositionProperty = PointerProperty(type=OOTCameraPositionProperty)
    Material.ootCollisionProperty = PointerProperty(type=OOTMaterialCollisionProperty)


def oot_col_unregister():
    for cls in reversed(oot_col_classes):
        unregister_class(cls)
