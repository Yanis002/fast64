import bpy

from dataclasses import dataclass
from typing import TYPE_CHECKING
from bpy.types import Object, CollectionProperty
from ..utility import PluginError, upgrade_prop, get_upgrade_data, can_upgrade
from ..data import Z64_ObjectData
from .utility import getEvalParams, get_actor_prop_from_obj
from ..game_data import game_data
from .cutscene.constants import ootEnumCSMotionCamMode

if TYPE_CHECKING:
    from .cutscene.properties import OOTCutsceneProperty


#####################################
# Room Header
#####################################
def upgradeObjectList(objList: CollectionProperty, objData: Z64_ObjectData):
    """Transition to the XML object system"""
    for obj in objList:
        # In order to check whether the data in the current blend needs to be updated,
        # we look for the ``objectID`` property, which has been removed in the current version.
        # If we find ``objectID`` it means that it's an old blend and needs be updated.
        # Finally, after the update we remove this property to tell Fast64 the object property is now up-to-date.

        if can_upgrade(obj, "objectID"):
            data = get_upgrade_data(obj)

            # ``obj["objectID"]`` returns the index inside ``ootEnumObjectIDLegacy``
            # since Blender saves the index of the element of the EnumProperty
            objectID = objData.ootEnumObjectIDLegacy[data["objectID"]][0]

            if objectID == "Custom":
                value = objectID
            else:
                value = objData.objects_by_id[objectID].key

            upgrade_prop(data, "objectID", obj, "objectKey", value)


def upgradeRoomHeaders(roomObj: Object, objData: Z64_ObjectData):
    """Main upgrade logic for room headers"""
    altHeaders = roomObj.ootAlternateRoomHeaders
    for sceneLayer in [
        roomObj.ootRoomHeader,
        altHeaders.childNightHeader,
        altHeaders.adultDayHeader,
        altHeaders.adultNightHeader,
    ]:
        if sceneLayer is not None:
            upgradeObjectList(sceneLayer.objectList, objData)
    for i in range(len(altHeaders.cutsceneHeaders)):
        upgradeObjectList(altHeaders.cutsceneHeaders[i].objectList, objData)


#####################################
# Cutscene
#####################################
@dataclass
class Cutscene_UpgradeData:
    oldPropName: str
    newPropName: str
    enumData: list[tuple[str, str, str]]  # this is the list used for enum properties


def transferOldDataToNew(data_holder, oldDataToNewData: dict[str, str]):
    # conversion to the same prop type
    # simply transfer the old data to the new one
    for oldName, newName in oldDataToNewData.items():
        data = get_upgrade_data(data_holder)

        if can_upgrade(data, oldName):
            if newName is not None:
                value = data[oldName]

                # special case for rumble subprops where it's a string to int conversion
                # another special case for light setting index where the value need to be minus one
                if newName in ["rumbleSourceStrength", "rumbleDuration", "rumbleDecreaseRate"]:
                    value = int(getEvalParams(data[oldName]), base=16)
                elif newName == "lightSettingsIndex":
                    value -= 1

                data[newName] = value

            data.property_unset(oldName)


def convertOldDataToEnumData(data_holder, oldDataToEnumData: list[Cutscene_UpgradeData]):
    data = get_upgrade_data(data_holder)

    # conversion to another prop type
    for csUpgradeData in oldDataToEnumData:
        if csUpgradeData.oldPropName in data:
            # get the old data
            oldData = get_upgrade_data(data, csUpgradeData.oldPropName)
            isUpgraded = False

            # if anything goes wrong there set the value to custom to avoid any data loss
            try:
                if isinstance(oldData, str):
                    # get the value, doing an eval for strings
                    value = int(getEvalParams(oldData), base=16)

                    # special cases for ocarina action enum
                    # since we don't have everything the value need to be shifted
                    if csUpgradeData.newPropName == "ocarinaAction":
                        if value in [0x00, 0x01, 0x0E, 0x1B]:
                            raise IndexError

                        # account for custom elements in the enums by adding 1
                        value += 1

                    if csUpgradeData.newPropName == "csSeqID":
                        # the old fade out value is wrong, it assumes it's a seq id
                        # but it's not, it's a seq player id,
                        # hence why we raise an error so it defaults to "custom" to avoid any data loss
                        # @TODO: find a way to check properly which seq command it is
                        raise NotImplementedError
                elif isinstance(oldData, int):
                    value = oldData

                    # another special case, this time for the misc enum
                    if csUpgradeData.newPropName == "csMiscType":
                        if value in [0x00, 0x04, 0x05]:
                            raise IndexError

                    # account for custom elements in the enums by adding 1
                    value += 1
                else:
                    raise NotImplementedError

                # if the value is in the list find the identifier
                if value < len(csUpgradeData.enumData):
                    setattr(data, csUpgradeData.newPropName, csUpgradeData.enumData[value][0])
                    isUpgraded = True
                else:
                    # else raise an error to default to custom
                    raise IndexError
            except:
                setattr(data, csUpgradeData.newPropName, "Custom")
                setattr(data, f"{csUpgradeData.newPropName}Custom", str(oldData))

                # @TODO: find a way to check properly which seq command it is
                if csUpgradeData.newPropName == "csSeqID":
                    setattr(data, "csSeqPlayer", "Custom")
                    setattr(data, "csSeqPlayerCustom", str(oldData))
                isUpgraded = True

            if isUpgraded:
                data.property_unset(csUpgradeData.oldPropName)
            else:
                raise PluginError(f"ERROR: ``{csUpgradeData.newPropName}`` did not upgrade properly!")


def upgradeCutsceneSubProps(csListSubProp):
    # ``csListSubProp`` types: OOTCSTextProperty | OOTCSSeqProperty | OOTCSMiscProperty | OOTCSRumbleProperty
    # based on ``upgradeObjectList``

    subPropsOldToNew = {
        # TextBox
        "messageId": "textID",
        "topOptionBranch": "topOptionTextID",
        "bottomOptionBranch": "bottomOptionTextID",
        # Lighting
        "index": "lightSettingsIndex",
        # Rumble
        "unk2": "rumbleSourceStrength",
        "unk3": "rumbleDuration",
        "unk4": "rumbleDecreaseRate",
        # Unk (Deprecated)
        "unk": None,
        "unkType": None,
        "unk1": None,
        "unk2": None,
        "unk3": None,
        "unk4": None,
        "unk5": None,
        "unk6": None,
        "unk7": None,
        "unk8": None,
        "unk9": None,
        "unk10": None,
        "unk11": None,
        "unk12": None,
    }

    subPropsToEnum = [
        # TextBox
        Cutscene_UpgradeData("ocarinaSongAction", "ocarinaAction", game_data.z64.enums.enum_ocarina_song_action_id),
        Cutscene_UpgradeData("type", "csTextType", game_data.z64.enums.enum_cs_text_type),
        # Seq
        Cutscene_UpgradeData("value", "csSeqID", game_data.z64.enums.enum_seq_id),
        # Misc
        Cutscene_UpgradeData("operation", "csMiscType", game_data.z64.enums.enum_cs_misc_type),
    ]

    transferOldDataToNew(csListSubProp, subPropsOldToNew)
    convertOldDataToEnumData(csListSubProp, subPropsToEnum)


def upgradeCSListProps(csListProp):
    # ``csListProp`` type: ``OOTCSListProperty``

    csListPropOldToNew = {
        "textbox": "textList",
        "lighting": "lightSettingsList",
        "time": "timeList",
        "bgm": "seqList",
        "misc": "miscList",
        "nine": "rumbleList",
        "fxStartFrame": "transitionStartFrame",
        "fxEndFrame": "transitionEndFrame",
    }

    transferOldDataToNew(csListProp, csListPropOldToNew)

    # both are enums but the item list is different (the old one doesn't have a "custom" entry)
    convertOldDataToEnumData(
        csListProp, [Cutscene_UpgradeData("fxType", "transitionType", game_data.z64.enums.enum_cs_transition_type)]
    )


def upgradeCutsceneProperty(csProp: "OOTCutsceneProperty"):
    csPropOldToNew = {
        "csWriteTerminator": "csUseDestination",
        "csTermStart": "csDestinationStartFrame",
        "csTermEnd": None,
    }

    transferOldDataToNew(csProp, csPropOldToNew)
    convertOldDataToEnumData(
        csProp, [Cutscene_UpgradeData("csTermIdx", "csDestination", game_data.z64.enums.enum_cs_destination)]
    )


def upgradeCutsceneMotion(csMotionObj: Object):
    """Main upgrade logic for Cutscene Motion data from zcamedit"""
    objName = csMotionObj.name

    if csMotionObj.type == "EMPTY":
        csMotionProp = csMotionObj.ootCSMotionProperty
        data = get_upgrade_data(csMotionObj)

        if can_upgrade(data, "zc_alist") and ("Preview." in objName or "ActionList." in objName):
            legacyData = get_upgrade_data(csMotionObj, "zc_alist")
            emptyTypeSuffix = "List" if "ActionList." in objName else "Preview"
            csMotionObj.ootEmptyType = f"CS {'Player' if 'Link' in objName else 'Actor'} Cue {emptyTypeSuffix}"

            if can_upgrade(legacyData, "actor_id"):
                index = legacyData["actor_id"]
                if index >= 0:
                    cmdEnum = game_data.z64.enums.enumByKey["cs_cmd"]
                    cmdType = cmdEnum.item_by_index.get(index)
                    if cmdType is not None:
                        csMotionProp.actorCueListProp.commandType = cmdType.key
                    else:
                        csMotionProp.actorCueListProp.commandType = "Custom"
                        csMotionProp.actorCueListProp.commandTypeCustom = f"0x{index:04X}"
                legacyData.property_unset("actor_id")

            data.property_unset("zc_alist")

        if can_upgrade(data, "zc_apoint") and "Point." in objName:
            isPlayer = "Link" in csMotionObj.parent.name
            legacyData = get_upgrade_data(csMotionObj, "zc_apoint")
            csMotionObj.ootEmptyType = f"CS {'Player' if isPlayer else 'Actor'} Cue"

            upgrade_prop(legacyData, "start_frame", csMotionProp.actorCueProp, "cueStartFrame")

            if can_upgrade(legacyData, "action_id"):
                playerEnum = game_data.z64.enums.enumByKey["cs_player_cue_id"]
                item = None
                if isPlayer:
                    item = playerEnum.item_by_index.get(int(legacyData["action_id"], base=16))

                if isPlayer and item is not None:
                    csMotionProp.actorCueProp.playerCueID = item.key
                else:
                    csMotionProp.actorCueProp.cueActionID = legacyData["action_id"]
                data.property_unset("action_id")

            data.property_unset("zc_apoint")

    if csMotionObj.type == "ARMATURE":
        camShotProp = csMotionObj.data.ootCamShotProp
        armature_data = get_upgrade_data(csMotionObj.data)
        upgrade_prop(armature_data, "start_frame", camShotProp, "shotStartFrame")

        if can_upgrade(armature_data, "cam_mode"):
            value = ootEnumCSMotionCamMode[armature_data["cam_mode"]][0]
            upgrade_prop(armature_data, "cam_mode", camShotProp, "shotCamMode", value)

        for bone in csMotionObj.data.bones:
            camShotPointProp = bone.ootCamShotPointProp
            bone_data = get_upgrade_data(bone)
            upgrade_prop(bone_data, "frames", camShotPointProp, "shotPointFrame")
            upgrade_prop(bone_data, "fov", camShotPointProp, "shotPointViewAngle")
            upgrade_prop(bone_data, "camroll", camShotPointProp, "shotPointRoll")


#####################################
# Actors
#####################################
def upgradeActors(actorObj: Object):
    # parameters
    props = get_actor_prop_from_obj(actorObj)
    actorProp = get_upgrade_data(props)
    isCustom = False

    if actorObj.ootEmptyType == "Entrance":
        isCustom = actorObj.ootEntranceProperty.customActor
    else:
        value = game_data.z64.actors.ootEnumActorID[actorProp["actorID"]][0]
        upgrade_prop(actorProp, "actorID", props, "actor_id", value)
        upgrade_prop(actorProp, "actorIDCustom", props, "actor_id_custom")
        isCustom = props.actor_id == "Custom"

    if can_upgrade(actorProp, "actorParam"):
        if not isCustom:
            prop_name = "params"

            if getEvalParams(actorProp["actorParam"]) is None:
                props.actor_id_custom = props.actor_id
                props.actor_id = "Custom"
                prop_name = "params_custom"
        else:
            prop_name = "params_custom"

        setattr(props, prop_name, actorProp["actorParam"])
        actorProp.property_unset("actorParam")

    if actorObj.ootEmptyType == "Actor":
        custom = "_custom" if actorProp.actor_id == "Custom" else ""

        if isCustom:
            upgrade_prop(actorProp, "rotOverride", props, "rot_override")

        for rot in {"X", "Y", "Z"}:
            if actorProp.actor_id == "Custom" or actorProp.is_rotation_used(f"{rot}Rot"):
                if can_upgrade(actorProp, f"rotOverride{rot}"):
                    if getEvalParams(actorProp[f"rotOverride{rot}"]) is None:
                        custom = "_custom"

                        if props.actor_id != "Custom":
                            props.actor_id_custom = props.actor_id
                            props.params_custom = props.params
                            props.actor_id = "Custom"
                            props.rot_override = True

                    setattr(actorProp, f"rot_{rot.lower()}{custom}", actorProp[f"rotOverride{rot}"])
                    actorProp.property_unset(f"rotOverride{rot}")

    # room stuff
    if actorObj.ootEmptyType == "Entrance":
        entranceProp = actorObj.ootEntranceProperty

        for obj in bpy.data.objects:
            if obj.type == "EMPTY" and obj.ootEmptyType == "Room":
                if actorObj in obj.children_recursive:
                    entranceProp.tiedRoom = obj
                    break
    elif actorObj.ootEmptyType == "Transition Actor":
        # get room parent
        roomParent = None
        for obj in bpy.data.objects:
            if obj.type == "EMPTY" and obj.ootEmptyType == "Room" and actorObj in obj.children_recursive:
                roomParent = obj
                break

        # if it's ``None`` then this door actor is not parented to a room
        if roomParent is None:
            print("WARNING: Ignoring Door Actor not parented to a room")
            return

        transActorProp = actorObj.ootTransitionActorProperty
        data = get_upgrade_data(actorObj, "ootTransitionActorProperty")
        if can_upgrade(data, "dontTransition") or can_upgrade(data, "roomIndex"):
            # look for old data since we don't want to overwrite newer existing data
            transActorProp.fromRoom = roomParent

        # upgrade old props if present
        upgrade_prop(
            data, "dontTransition", transActorProp, "isRoomTransition", transActorProp["dontTransition"] == False
        )

        if can_upgrade(data, "roomIndex"):
            for obj in bpy.data.objects:
                if (
                    obj != transActorProp.fromRoom
                    and obj.type == "EMPTY"
                    and obj.ootEmptyType == "Room"
                    and obj.ootRoomHeader.roomIndex == transActorProp["roomIndex"]
                ):
                    transActorProp.toRoom = obj
                    transActorProp.property_unset("roomIndex")
                    break
