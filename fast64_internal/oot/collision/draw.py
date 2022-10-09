from bpy.types import UILayout, ID
from ...utility import prop_split
from ..oot_utility import drawEnumWithCustom
from .classes import OOTCameraPositionProperty, OOTMaterialCollisionProperty, OOTWaterBoxProperty


def drawWaterBoxProperty(layout: UILayout, waterBoxProp: OOTWaterBoxProperty, roomIndex: int):
    wBoxLayout = layout.column()

    wBoxLayout.prop(waterBoxProp, "isGlobal")

    if waterBoxProp.isGlobal:
        labelText = "This WaterBox is global to the current scene."
    elif roomIndex < 63:
        labelText = f"Room Index: {roomIndex}"
    else:
        # the code enforce a maximum for this index since
        # it's with other properties, see macros inside ``z64bgcheck.h``
        labelText = "The room index can't be higher than 62 (0x3E)!"

    wBoxLayout.label(text=labelText)
    prop_split(wBoxLayout, waterBoxProp, "lighting", "Lighting")
    prop_split(wBoxLayout, waterBoxProp, "camera", "Camera")
    wBoxLayout.label(text="Defined by top face of box empty.")
    wBoxLayout.label(text="No rotation allowed.")


def drawCameraProperty(camLayout: UILayout, camProp: OOTCameraPositionProperty, objData: ID):
    camLayout.box().label(text="Camera Data")
    drawEnumWithCustom(camLayout, camProp, "camSType", "Camera S Type", "")
    prop_split(camLayout, camProp, "index", "Camera Index")

    if camProp.hasPositionData:
        prop_split(camLayout, objData, "angle", "Field Of View")
        prop_split(camLayout, camProp, "jfifID", "JFIF ID")

    camLayout.prop(camProp, "hasPositionData")


def drawCollisionProperty(colLayout: UILayout, collisionProp: OOTMaterialCollisionProperty):
    prop_split(colLayout, collisionProp, "exitID", "Exit ID")
    prop_split(colLayout, collisionProp, "cameraID", "Camera ID")
    prop_split(colLayout, collisionProp, "echo", "Echo")
    prop_split(colLayout, collisionProp, "lightingSetting", "Lighting")

    drawEnumWithCustom(colLayout, collisionProp, "terrain", "Terrain", "")
    drawEnumWithCustom(colLayout, collisionProp, "sound", "Sound", "")

    colLayout.prop(collisionProp, "eponaBlock", text="Blocks Epona")
    colLayout.prop(collisionProp, "decreaseHeight", text="Decrease Height 1 Unit")
    colLayout.prop(collisionProp, "isWallDamage", text="Is Wall Damage")
    colLayout.prop(collisionProp, "hookshotable", text="Hookshotable")

    drawEnumWithCustom(colLayout, collisionProp, "floorSetting", "Floor Setting", "")
    drawEnumWithCustom(colLayout, collisionProp, "wallSetting", "Wall Setting", "")
    drawEnumWithCustom(colLayout, collisionProp, "floorProperty", "Floor Property", "")

    colLayout.prop(collisionProp, "ignoreCameraCollision", text="Ignore Camera Collision")
    colLayout.prop(collisionProp, "ignoreActorCollision", text="Ignore Actor Collision")
    colLayout.prop(collisionProp, "ignoreProjectileCollision", text="Ignore Projectile Collision")

    prop_split(colLayout, collisionProp, "conveyorOption", "Conveyor Option")

    if collisionProp.conveyorOption != "None":
        prop_split(colLayout, collisionProp, "conveyorRotation", "Conveyor Rotation")
        drawEnumWithCustom(colLayout, collisionProp, "conveyorSpeed", "Conveyor Speed", "")
        if collisionProp.conveyorSpeed != "Custom":
            colLayout.prop(collisionProp, "conveyorKeepMomentum", text="Keep Momentum")
