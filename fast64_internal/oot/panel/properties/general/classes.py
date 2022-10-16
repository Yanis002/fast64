from bpy.props import PointerProperty, IntProperty, EnumProperty
from bpy.types import Object, PropertyGroup
from bpy.utils import register_class, unregister_class
from .....utility import gammaInverse
from ..collision.classes import OOTWaterBoxProperty
from .actor.classes import OOTActorProperty, OOTTransitionActorProperty, OOTEntranceProperty
from .scene.operators import OOT_SearchSceneEnumOperator, OOT_SearchMusicSeqEnumOperator
from .scene.classes import OOTSceneProperties, OOTSceneHeaderProperty, OOTAlternateSceneHeaderProperty
from .room.operators import OOT_SearchObjectEnumOperator
from .room.classes import OOTRoomHeaderProperty, OOTAlternateRoomHeaderProperty
from .cutscene.operators import OOTCSTextboxAdd, OOTCSListAdd
from ....data import ootEnumEmptyType, ootRegisterQueue

from .cutscene.classes import (
    OOTCutsceneProperty,
    OOTCSTextboxProperty,
    OOTCSLightingProperty,
    OOTCSTimeProperty,
    OOTCSBGMProperty,
    OOTCSMiscProperty,
    OOTCS0x09Property,
    OOTCSUnkProperty,
    OOTCSListProperty,
)


def setLightPropertyValues(lightProp, ambient, diffuse0, diffuse1, fogColor, fogNear):
    lightProp.ambient = gammaInverse([value / 255 for value in ambient]) + [1]
    lightProp.diffuse0 = gammaInverse([value / 255 for value in diffuse0]) + [1]
    lightProp.diffuse1 = gammaInverse([value / 255 for value in diffuse1]) + [1]
    lightProp.fogColor = gammaInverse([value / 255 for value in fogColor]) + [1]
    lightProp.fogNear = fogNear


def onUpdateOOTEmptyType(self, context):
    isNoneEmpty = self.ootEmptyType == "None"
    isBoxEmpty = self.ootEmptyType == "Water Box"
    isSphereEmpty = self.ootEmptyType == "Cull Group"
    self.show_name = not (isBoxEmpty or isNoneEmpty or isSphereEmpty)
    self.show_axis = not (isBoxEmpty or isNoneEmpty or isSphereEmpty)

    if isBoxEmpty:
        self.empty_display_type = "CUBE"

    if isSphereEmpty:
        self.empty_display_type = "SPHERE"

    if self.ootEmptyType == "Scene":
        if len(self.ootSceneHeader.lightList) == 0:
            light = self.ootSceneHeader.lightList.add()
        if not self.ootSceneHeader.timeOfDayLights.defaultsSet:
            self.ootSceneHeader.timeOfDayLights.defaultsSet = True
            timeOfDayLights = self.ootSceneHeader.timeOfDayLights
            setLightPropertyValues(
                timeOfDayLights.dawn, [70, 45, 57], [180, 154, 138], [20, 20, 60], [140, 120, 100], 0x3E1
            )
            setLightPropertyValues(
                timeOfDayLights.day, [105, 90, 90], [255, 255, 240], [50, 50, 90], [100, 100, 120], 0x3E4
            )
            setLightPropertyValues(
                timeOfDayLights.dusk, [120, 90, 0], [250, 135, 50], [30, 30, 60], [120, 70, 50], 0x3E3
            )
            setLightPropertyValues(timeOfDayLights.night, [40, 70, 100], [20, 20, 35], [50, 50, 100], [0, 0, 30], 0x3E0)


class OOT_ObjectProperties(PropertyGroup):
    version: IntProperty(name="OOT_ObjectProperties Version", default=0)
    cur_version = 0  # version after property migration

    scene: PointerProperty(type=OOTSceneProperties)


oot_obj_classes = [
    OOTSceneProperties,
    OOT_ObjectProperties,
    OOT_SearchMusicSeqEnumOperator,
    OOT_SearchObjectEnumOperator,
    OOT_SearchSceneEnumOperator,
    OOTCSTextboxProperty,
    OOTCSTextboxAdd,
    OOTCSLightingProperty,
    OOTCSTimeProperty,
    OOTCSBGMProperty,
    OOTCSMiscProperty,
    OOTCS0x09Property,
    OOTCSUnkProperty,
    OOTCSListProperty,
    OOTCSListAdd,
    OOTCutsceneProperty,
]


def oot_obj_register():
    oot_obj_classes.extend(ootRegisterQueue)

    for cls in oot_obj_classes:
        register_class(cls)

    Object.ootEmptyType = EnumProperty(
        name="OOT Object Type", items=ootEnumEmptyType, default="None", update=onUpdateOOTEmptyType
    )

    Object.ootActorProperty = PointerProperty(type=OOTActorProperty)
    Object.ootTransitionActorProperty = PointerProperty(type=OOTTransitionActorProperty)
    Object.ootWaterBoxProperty = PointerProperty(type=OOTWaterBoxProperty)
    Object.ootRoomHeader = PointerProperty(type=OOTRoomHeaderProperty)
    Object.ootSceneHeader = PointerProperty(type=OOTSceneHeaderProperty)
    Object.ootAlternateSceneHeaders = PointerProperty(type=OOTAlternateSceneHeaderProperty)
    Object.ootAlternateRoomHeaders = PointerProperty(type=OOTAlternateRoomHeaderProperty)
    Object.ootEntranceProperty = PointerProperty(type=OOTEntranceProperty)
    Object.ootCutsceneProperty = PointerProperty(type=OOTCutsceneProperty)


def oot_obj_unregister():

    del Object.ootEmptyType

    del Object.ootActorProperty
    del Object.ootTransitionActorProperty
    del Object.ootWaterBoxProperty
    del Object.ootRoomHeader
    del Object.ootSceneHeader
    del Object.ootAlternateSceneHeaders
    del Object.ootAlternateRoomHeaders
    del Object.ootEntranceProperty
    del Object.ootCutsceneProperty

    for cls in reversed(oot_obj_classes):
        unregister_class(cls)
