import bpy

from dataclasses import dataclass, field
from bpy.types import Object
from typing import Optional
from ..utility import is_oot_features, is_game_oot
from ..constants import oot_data, mm_data
from .motion.utility import getBlenderPosition, getBlenderRotation, getRotation, getInteger


def cs_import_float(v_str: str):
    return float(v_str.removesuffix("f"))


# NOTE: ``paramNumber`` is the expected number of parameters inside the parsed commands,
# this account for the unused parameters. Every classes are based on the commands arguments from ``z64cutscene_commands.h``
#
# some commands have a `size` attribute, it's purpose is for the exporter as
# MM's camera command requires the size of the camera data in bytes


@dataclass
class CutsceneCmdBase:
    """This class contains common Cutscene data"""

    params: list[str]

    startFrame: Optional[int] = None
    endFrame: Optional[int] = None

    # MM doesn't have startFrame and endFrame, instead it's just the framecount
    duration: Optional[int] = None

    def getEnumValue(self, enumKey: str, index: int, isSeqLegacy: bool = False):
        if not is_game_oot() and enumKey not in {"seqId", "destinationType", "ocarinaSongActionId", "motionBlurType", "modifySeqType", "chooseCreditsSceneType", "transitionGeneralType"}:
            # remove `cs` and lowercase first letter
            enumKey = enumKey[2].lower() + enumKey[3:]

        enum = oot_data.enumData.enumByKey[enumKey] if is_game_oot() else mm_data.enum_data.enum_by_key[enumKey]
        item = enum.item_by_id.get(self.params[index])
        if item is None:
            setting = getInteger(self.params[index])
            if isSeqLegacy:
                setting -= 1
            item = enum.item_by_index.get(setting)
        return item.key if item is not None else self.params[index]


@dataclass
class CutsceneCmdCamPoint(CutsceneCmdBase):
    """This class contains a single Camera Point command data"""

    continueFlag: Optional[str] = None
    camRoll: Optional[int] = None
    frame: Optional[int] = None
    viewAngle: Optional[float] = None
    pos: list[int] = field(default_factory=list)
    paramNumber: int = 8

    def __post_init__(self):
        if self.params is not None:
            self.continueFlag = self.params[0]
            self.camRoll = getInteger(self.params[1])
            self.frame = getInteger(self.params[2])
            self.viewAngle = cs_import_float(self.params[3])
            self.pos = [getInteger(self.params[4]), getInteger(self.params[5]), getInteger(self.params[6])]


# MM's new camera commands

@dataclass
class CutsceneCmdNewCamPoint(CutsceneCmdBase):
    """This class contains a single Camera Point command data (the newer version)"""

    interp_type: Optional[str] = None
    weight: Optional[int] = None
    pos: list[int] = field(default_factory=list)
    relative_to: Optional[str] = None
    paramNumber: int = 7
    size: int = 0xC

    def __post_init__(self):
        if self.params is not None:
            self.interp_type = self.params[0]
            self.weight = getInteger(self.params[1])
            self.duration = getInteger(self.params[2])
            self.pos = [getInteger(self.params[3]), getInteger(self.params[4]), getInteger(self.params[5])]
            self.relative_to = self.params[6]


@dataclass
class CutsceneCmdCamMisc(CutsceneCmdBase):
    """This class contains the Camera Misc data"""

    camRoll: Optional[int] = None
    viewAngle: Optional[float] = None
    paramNumber: int = 4
    size: int = 0x8

    def __post_init__(self):
        if self.params is not None:
            self.camRoll = getInteger(self.params[1])
            self.viewAngle = getInteger(self.params[2])


@dataclass
class CutsceneSplinePoint:
    # this is not a real command but it helps as each camera point is made of one at, one eye and one misc
    at: Optional[CutsceneCmdNewCamPoint] = None
    eye: Optional[CutsceneCmdNewCamPoint] = None
    misc: Optional[CutsceneCmdCamMisc] = None


@dataclass
class CutsceneCmdCamSpline(CutsceneCmdBase):
    """This class contains the Camera Spline data"""

    num_entries: Optional[int] = None
    entries: list[CutsceneSplinePoint] = field(default_factory=list)
    paramNumber: int = 4
    size: int = 0x8

    def __post_init__(self):
        if self.params is not None:
            self.num_entries = getInteger(self.params[0])
            self.duration = getInteger(self.params[3])


@dataclass
class CutsceneCmdCamSplineList(CutsceneCmdBase):
    """This class contains the Camera Spline list data"""

    num_bytes: Optional[int] = None
    entries: list[CutsceneCmdCamSpline] = field(default_factory=list)
    paramNumber: int = 1
    listName: str = "camSplineListNew"
    size: int = 0x8

    def __post_init__(self):
        if self.params is not None:
            self.num_bytes = getInteger(self.params[0])


@dataclass
class CutsceneCmdActorCue(CutsceneCmdBase):
    """This class contains a single Actor Cue command data"""

    actionID: Optional[int | str] = None
    rot: list[str] = field(default_factory=list)
    startPos: list[int] = field(default_factory=list)
    endPos: list[int] = field(default_factory=list)
    paramNumber: int = 15

    def __post_init__(self):
        if self.params is not None:
            self.startFrame = getInteger(self.params[1])
            self.endFrame = getInteger(self.params[2])
            try:
                self.actionID = getInteger(self.params[0])
            except ValueError:
                self.actionID = self.params[0]
            self.rot = [getRotation(self.params[3]), getRotation(self.params[4]), getRotation(self.params[5])]
            self.startPos = [getInteger(self.params[6]), getInteger(self.params[7]), getInteger(self.params[8])]
            self.endPos = [getInteger(self.params[9]), getInteger(self.params[10]), getInteger(self.params[11])]


@dataclass
class CutsceneCmdActorCueList(CutsceneCmdBase):
    """This class contains the Actor Cue List command data"""

    isPlayer: bool = False
    commandType: Optional[str] = None
    entryTotal: Optional[int] = None
    entries: list[CutsceneCmdActorCue] = field(default_factory=list)
    paramNumber: int = 2
    listName: str = "actorCueList"

    def __post_init__(self):
        if self.params is not None:
            if self.isPlayer:
                self.commandType = "Player"
                self.entryTotal = getInteger(self.params[0])
            else:
                self.commandType = self.params[0]
                if self.commandType.startswith("0x"):
                    # make it a 4 digit hex
                    self.commandType = self.commandType.removeprefix("0x")
                    self.commandType = "0x" + "0" * (4 - len(self.commandType)) + self.commandType
                else:
                    if is_game_oot():
                        self.commandType = oot_data.enumData.enumByKey["csCmd"].item_by_id[self.commandType].key
                    else:
                        self.commandType = mm_data.enum_data.enum_by_key["cmd"].item_by_id[self.commandType].key
                self.entryTotal = getInteger(self.params[1].strip())


@dataclass
class CutsceneCmdCamEyeSpline(CutsceneCmdBase):
    """This class contains the Camera Eye Spline data"""

    entries: list[CutsceneCmdCamPoint] = field(default_factory=list)
    paramNumber: int = 2
    listName: str = "camEyeSplineList"

    def __post_init__(self):
        if self.params is not None:
            self.startFrame = getInteger(self.params[0])
            self.endFrame = getInteger(self.params[1])


@dataclass
class CutsceneCmdCamATSpline(CutsceneCmdBase):
    """This class contains the Camera AT (look-at) Spline data"""

    entries: list[CutsceneCmdCamPoint] = field(default_factory=list)
    paramNumber: int = 2
    listName: str = "camATSplineList"

    def __post_init__(self):
        if self.params is not None:
            self.startFrame = getInteger(self.params[0])
            self.endFrame = getInteger(self.params[1])


@dataclass
class CutsceneCmdCamEyeSplineRelToPlayer(CutsceneCmdBase):
    """This class contains the Camera Eye Spline Relative to the Player data"""

    entries: list[CutsceneCmdCamPoint] = field(default_factory=list)
    paramNumber: int = 2
    listName: str = "camEyeSplineRelPlayerList"

    def __post_init__(self):
        if self.params is not None:
            self.startFrame = getInteger(self.params[0])
            self.endFrame = getInteger(self.params[1])


@dataclass
class CutsceneCmdCamATSplineRelToPlayer(CutsceneCmdBase):
    """This class contains the Camera AT Spline Relative to the Player data"""

    entries: list[CutsceneCmdCamPoint] = field(default_factory=list)
    paramNumber: int = 2
    listName: str = "camATSplineRelPlayerList"

    def __post_init__(self):
        if self.params is not None:
            self.startFrame = getInteger(self.params[0])
            self.endFrame = getInteger(self.params[1])


@dataclass
class CutsceneCmdCamEye(CutsceneCmdBase):
    """This class contains a single Camera Eye point"""

    # This feature is not used in the final game and lacks polish, it is recommended to use splines in all cases.
    entries: list = field(default_factory=list)
    paramNumber: int = 2
    listName: str = "camEyeList"

    def __post_init__(self):
        if self.params is not None:
            self.startFrame = getInteger(self.params[0])
            self.endFrame = getInteger(self.params[1])


@dataclass
class CutsceneCmdCamAT(CutsceneCmdBase):
    """This class contains a single Camera AT point"""

    # This feature is not used in the final game and lacks polish, it is recommended to use splines in all cases.
    entries: list = field(default_factory=list)
    paramNumber: int = 2
    listName: str = "camATList"

    def __post_init__(self):
        if self.params is not None:
            self.startFrame = getInteger(self.params[0])
            self.endFrame = getInteger(self.params[1])


@dataclass
class CutsceneCmdMisc(CutsceneCmdBase):
    """This class contains a single misc command entry"""

    type: Optional[str] = None  # see `CutsceneMiscType` in decomp
    paramNumber: int = 14

    def __post_init__(self):
        if self.params is not None:
            self.startFrame = getInteger(self.params[1])
            self.endFrame = getInteger(self.params[2])
            self.type = self.getEnumValue("csMiscType", 0)


@dataclass
class CutsceneCmdMiscList(CutsceneCmdBase):
    """This class contains Misc command data"""

    entryTotal: Optional[int] = None
    entries: list[CutsceneCmdMisc] = field(default_factory=list)
    paramNumber: int = 1
    listName: str = "miscList"

    def __post_init__(self):
        if self.params is not None:
            self.entryTotal = getInteger(self.params[0])


@dataclass
class CutsceneCmdTransition(CutsceneCmdBase):
    """This class contains Transition command data"""

    type: Optional[str] = None
    paramNumber: int = 3
    listName: str = "transitionList"

    def __post_init__(self):
        if self.params is not None:
            self.startFrame = getInteger(self.params[1])
            self.endFrame = getInteger(self.params[2])
            self.type = self.getEnumValue("csTransitionType", 0)


@dataclass
class CutsceneCmdTransitionList(CutsceneCmdBase):
    """This class contains Transition list command data"""

    entryTotal: Optional[int] = None
    entries: list[CutsceneCmdTransition] = field(default_factory=list)
    paramNumber: int = 1
    listName: str = "transitionListNew"

    def __post_init__(self):
        if self.params is not None:
            self.entryTotal = getInteger(self.params[0])


@dataclass
class CutsceneCmdText(CutsceneCmdBase):
    """This class contains Text command data"""

    textId: Optional[int] = None
    type: Optional[str] = None
    altTextId1: Optional[int] = None
    altTextId2: Optional[int] = None
    paramNumber: int = 6
    id: str = "Text"

    def __post_init__(self):
        if self.params is not None:
            self.startFrame = getInteger(self.params[1])
            self.endFrame = getInteger(self.params[2])
            self.textId = getInteger(self.params[0])
            self.type = self.getEnumValue("csTextType", 3)
            self.altTextId1 = getInteger(self.params[4])
            self.altTextId2 = getInteger(self.params[5])


@dataclass
class CutsceneCmdTextNone(CutsceneCmdBase):
    """This class contains Text None command data"""

    paramNumber: int = 2
    id: str = "None"

    def __post_init__(self):
        if self.params is not None:
            self.startFrame = getInteger(self.params[0])
            self.endFrame = getInteger(self.params[1])


@dataclass
class CutsceneCmdTextOcarinaAction(CutsceneCmdBase):
    """This class contains Text Ocarina Action command data"""

    ocarinaActionId: Optional[str] = None
    messageId: Optional[int] = None
    paramNumber: int = 4
    id: str = "OcarinaAction"

    def __post_init__(self):
        if self.params is not None:
            self.startFrame = getInteger(self.params[1])
            self.endFrame = getInteger(self.params[2])
            self.ocarinaActionId = self.getEnumValue("ocarinaSongActionId", 0)
            self.messageId = getInteger(self.params[3])


@dataclass
class CutsceneCmdTextGeneric(CutsceneCmdBase):
    """This class contains generic text command data"""

    textId: Optional[int] = None
    topOptionBranch: Optional[int] = None
    bottomOptionBranch: Optional[int] = None
    paramNumber: int = 5
    id: str = "Generic"

    def __post_init__(self):
        if self.params is not None:
            self.textId = getInteger(self.params[0])
            self.startFrame = getInteger(self.params[1])
            self.endFrame = getInteger(self.params[2])
            self.topOptionBranch = getInteger(self.params[3])
            self.bottomOptionBranch = getInteger(self.params[4])


@dataclass
class CutsceneCmdTextMask(CutsceneCmdBase):
    """This class contains mask/remains text command data"""

    defaultTextId: Optional[int] = None
    alternativeTextId: Optional[int] = None
    paramNumber: int = 4
    id: str = "Mask"

    def __post_init__(self):
        if self.params is not None:
            self.defaultTextId = getInteger(self.params[0])
            self.startFrame = getInteger(self.params[1])
            self.endFrame = getInteger(self.params[2])
            self.alternativeTextId = getInteger(self.params[3])


@dataclass
class CutsceneCmdTextList(CutsceneCmdBase):
    """This class contains Text List command data"""

    entryTotal: Optional[int] = None
    entries: list[CutsceneCmdText | CutsceneCmdTextNone | CutsceneCmdTextOcarinaAction | CutsceneCmdTextGeneric | CutsceneCmdTextMask] = field(default_factory=list)
    paramNumber: int = 1
    listName: str = "textList"

    def __post_init__(self):
        if self.params is not None:
            self.entryTotal = getInteger(self.params[0])


@dataclass
class CutsceneCmdLightSetting(CutsceneCmdBase):
    """This class contains Light Setting command data"""

    isLegacy: Optional[bool] = None
    lightSetting: Optional[int] = None
    paramNumber: int = 14

    def __post_init__(self):
        if self.params is not None:
            self.startFrame = getInteger(self.params[1])
            self.endFrame = getInteger(self.params[2])
            self.lightSetting = getInteger(self.params[0])
            if self.isLegacy:
                self.lightSetting -= 1


@dataclass
class CutsceneCmdLightSettingList(CutsceneCmdBase):
    """This class contains Light Setting List command data"""

    entryTotal: Optional[int] = None
    entries: list[CutsceneCmdLightSetting] = field(default_factory=list)
    paramNumber: int = 1
    listName: str = "lightSettingsList"

    def __post_init__(self):
        if self.params is not None:
            self.entryTotal = getInteger(self.params[0])


@dataclass
class CutsceneCmdTime(CutsceneCmdBase):
    """This class contains Time Ocarina Action command data"""

    hour: Optional[int] = None
    minute: Optional[int] = None
    paramNumber: int = 5

    def __post_init__(self):
        if self.params is not None:
            self.startFrame = getInteger(self.params[1])
            self.endFrame = getInteger(self.params[2])
            self.hour = getInteger(self.params[3])
            self.minute = getInteger(self.params[4])


@dataclass
class CutsceneCmdTimeList(CutsceneCmdBase):
    """This class contains Time List command data"""

    entryTotal: Optional[int] = None
    entries: list[CutsceneCmdTime] = field(default_factory=list)
    paramNumber: int = 1
    listName: str = "timeList"

    def __post_init__(self):
        if self.params is not None:
            self.entryTotal = getInteger(self.params[0])


@dataclass
class CutsceneCmdStartStopSeq(CutsceneCmdBase):
    """This class contains Start/Stop Seq command data"""

    isLegacy: Optional[bool] = None
    seqId: Optional[str] = None
    paramNumber: int = 11

    def __post_init__(self):
        if self.params is not None:
            self.startFrame = getInteger(self.params[1])
            self.endFrame = getInteger(self.params[2])
            self.seqId = self.getEnumValue("seqId", 0, self.isLegacy)


@dataclass
class CutsceneCmdStartStopSeqList(CutsceneCmdBase):
    """This class contains Start/Stop Seq List command data"""

    entryTotal: Optional[int] = None
    type: Optional[str] = None
    entries: list[CutsceneCmdStartStopSeq] = field(default_factory=list)
    paramNumber: int = 1
    listName: str = "seqList"

    def __post_init__(self):
        if self.params is not None:
            self.entryTotal = getInteger(self.params[0])


@dataclass
class CutsceneCmdFadeSeq(CutsceneCmdBase):
    """This class contains Fade Seq command data"""

    seqPlayer: Optional[str] = None
    paramNumber: int = 11
    enumKey: str = "csFadeOutSeqPlayer"

    def __post_init__(self):
        if self.params is not None:
            self.startFrame = getInteger(self.params[1])
            self.endFrame = getInteger(self.params[2])
            self.seqPlayer = self.getEnumValue("csFadeOutSeqPlayer", 0)


@dataclass
class CutsceneCmdFadeSeqList(CutsceneCmdBase):
    """This class contains Fade Seq List command data"""

    entryTotal: Optional[int] = None
    entries: list[CutsceneCmdFadeSeq] = field(default_factory=list)
    paramNumber: int = 1
    listName: str = "fadeSeqList"

    def __post_init__(self):
        if self.params is not None:
            self.entryTotal = getInteger(self.params[0])


@dataclass
class CutsceneCmdRumbleController(CutsceneCmdBase):
    """This class contains Rumble Controller command data"""

    sourceStrength: Optional[int] = None
    duration: Optional[int] = None
    decreaseRate: Optional[int] = None
    paramNumber: int = 8

    def __post_init__(self):
        if self.params is not None:
            self.startFrame = getInteger(self.params[1])
            self.endFrame = getInteger(self.params[2])
            self.sourceStrength = getInteger(self.params[3])
            self.duration = getInteger(self.params[4])
            self.decreaseRate = getInteger(self.params[5])


@dataclass
class CutsceneCmdRumbleControllerList(CutsceneCmdBase):
    """This class contains Rumble Controller List command data"""

    entryTotal: Optional[int] = None
    entries: list[CutsceneCmdRumbleController] = field(default_factory=list)
    paramNumber: int = 1
    listName: str = "rumbleList"

    def __post_init__(self):
        if self.params is not None:
            self.entryTotal = getInteger(self.params[0])


@dataclass
class CutsceneCmdDestination(CutsceneCmdBase):
    """This class contains Destination command data"""

    type: Optional[str] = None
    paramNumber: int = 3
    listName: str = "destination"

    def __post_init__(self):
        if self.params is not None:
            self.type = self.getEnumValue("csDestination" if is_game_oot() else "destinationType", 0)
            self.startFrame = getInteger(self.params[1])


@dataclass
class CutsceneCmdDestinationList(CutsceneCmdBase):
    """This class contains Destination list command data"""

    entryTotal: Optional[int] = None
    entries: list[CutsceneCmdDestination] = field(default_factory=list)
    paramNumber: int = 1
    listName: str = "destinationListNew"

    def __post_init__(self):
        if self.params is not None:
            self.entryTotal = getInteger(self.params[0])


@dataclass
class CutsceneCmdMotionBlur(CutsceneCmdBase):
    """This class contains motion blur command data"""

    type: Optional[str] = None
    paramNumber: int = 3

    def __post_init__(self):
        if self.params is not None:
            self.type = self.getEnumValue("motionBlurType", 0)
            self.startFrame = getInteger(self.params[1])
            self.endFrame = getInteger(self.params[2])


@dataclass
class CutsceneCmdMotionBlurList(CutsceneCmdBase):
    """This class contains motion blur list command data"""

    entryTotal: Optional[int] = None
    entries: list[CutsceneCmdDestination] = field(default_factory=list)
    paramNumber: int = 1
    listName: str = "motionBlurList"

    def __post_init__(self):
        if self.params is not None:
            self.entryTotal = getInteger(self.params[0])


@dataclass
class CutsceneCmdModifySeq(CutsceneCmdBase):
    """This class contains modify seq command data"""

    type: Optional[str] = None
    paramNumber: int = 3

    def __post_init__(self):
        if self.params is not None:
            self.type = self.getEnumValue("modifySeqType", 0)
            self.startFrame = getInteger(self.params[1])
            self.endFrame = getInteger(self.params[2])


@dataclass
class CutsceneCmdModifySeqList(CutsceneCmdBase):
    """This class contains modify seq list command data"""

    entryTotal: Optional[int] = None
    entries: list[CutsceneCmdModifySeq] = field(default_factory=list)
    paramNumber: int = 1
    listName: str = "modifySeqList"

    def __post_init__(self):
        if self.params is not None:
            self.entryTotal = getInteger(self.params[0])


@dataclass
class CutsceneCmdChooseCreditsScenes(CutsceneCmdBase):
    """This class contains choose credits scenes command data"""

    type: Optional[str] = None
    paramNumber: int = 3

    def __post_init__(self):
        if self.params is not None:
            self.type = self.getEnumValue("chooseCreditsSceneType", 0)
            self.startFrame = getInteger(self.params[1])
            self.endFrame = getInteger(self.params[2])


@dataclass
class CutsceneCmdChooseCreditsScenesList(CutsceneCmdBase):
    """This class contains choose credits scenes list command data"""

    entryTotal: Optional[int] = None
    entries: list[CutsceneCmdChooseCreditsScenes] = field(default_factory=list)
    paramNumber: int = 1
    listName: str = "creditsSceneList"

    def __post_init__(self):
        if self.params is not None:
            self.entryTotal = getInteger(self.params[0])


@dataclass
class CutsceneCmdTransitionGeneral(CutsceneCmdBase):
    """This class contains transition general command data"""

    type: Optional[str] = None
    rgb: list[int] = field(default_factory=list)
    paramNumber: int = 6

    def __post_init__(self):
        if self.params is not None:
            self.type = self.getEnumValue("transitionGeneralType", 0)
            self.startFrame = getInteger(self.params[1])
            self.endFrame = getInteger(self.params[2])
            self.rgb = [getInteger(self.params[3]), getInteger(self.params[4]), getInteger(self.params[5])]


@dataclass
class CutsceneCmdTransitionGeneralList(CutsceneCmdBase):
    """This class contains transition general list command data"""

    entryTotal: Optional[int] = None
    entries: list[CutsceneCmdTransitionGeneral] = field(default_factory=list)
    paramNumber: int = 1
    listName: str = "transitionGeneralList"

    def __post_init__(self):
        if self.params is not None:
            self.entryTotal = getInteger(self.params[0])


@dataclass
class CutsceneCmdGiveTatl(CutsceneCmdBase):
    """This class contains give tatl command data"""

    giveTatl: Optional[bool] = None
    paramNumber: int = 3

    def __post_init__(self):
        if self.params is not None:
            self.giveTatl = self.params[0] in {"true", "1"}
            self.startFrame = getInteger(self.params[1])
            self.endFrame = getInteger(self.params[2])


@dataclass
class CutsceneCmdGiveTatlList(CutsceneCmdBase):
    """This class contains give tatl list command data"""

    entryTotal: Optional[int] = None
    entries: list[CutsceneCmdGiveTatl] = field(default_factory=list)
    paramNumber: int = 1
    listName: str = "giveTatlList"

    def __post_init__(self):
        if self.params is not None:
            self.entryTotal = getInteger(self.params[0])


@dataclass
class Cutscene:
    """This class contains a Cutscene's data, including every commands' data"""

    name: str
    totalEntries: int
    frameCount: int
    paramNumber: int = 2

    destination: CutsceneCmdDestination = None
    actorCueList: list[CutsceneCmdActorCueList] = field(default_factory=list)
    playerCueList: list[CutsceneCmdActorCueList] = field(default_factory=list)
    camEyeSplineList: list[CutsceneCmdCamEyeSpline] = field(default_factory=list)
    camATSplineList: list[CutsceneCmdCamATSpline] = field(default_factory=list)
    camEyeSplineRelPlayerList: list[CutsceneCmdCamEyeSplineRelToPlayer] = field(default_factory=list)
    camATSplineRelPlayerList: list[CutsceneCmdCamATSplineRelToPlayer] = field(default_factory=list)
    camEyeList: list[CutsceneCmdCamEye] = field(default_factory=list)
    camATList: list[CutsceneCmdCamAT] = field(default_factory=list)
    textList: list[CutsceneCmdTextList] = field(default_factory=list)
    miscList: list[CutsceneCmdMiscList] = field(default_factory=list)
    rumbleList: list[CutsceneCmdRumbleControllerList] = field(default_factory=list)
    transitionList: list[CutsceneCmdTransition] = field(default_factory=list) 
    lightSettingsList: list[CutsceneCmdLightSettingList] = field(default_factory=list)
    timeList: list[CutsceneCmdTimeList] = field(default_factory=list)
    seqList: list[CutsceneCmdStartStopSeqList] = field(default_factory=list)
    fadeSeqList: list[CutsceneCmdFadeSeqList] = field(default_factory=list)

    # lists from the new cutscene system
    camSplineListNew: list[CutsceneCmdCamSplineList] = field(default_factory=list)
    transitionListNew: list[CutsceneCmdTransitionList] = field(default_factory=list)
    destinationListNew: list[CutsceneCmdDestinationList] = field(default_factory=list)
    motionBlurList: list[CutsceneCmdMotionBlurList] = field(default_factory=list)
    modifySeqList: list[CutsceneCmdModifySeqList] = field(default_factory=list)
    creditsSceneList: list[CutsceneCmdChooseCreditsScenesList] = field(default_factory=list)
    transitionGeneralList: list[CutsceneCmdTransitionGeneralList] = field(default_factory=list)
    giveTatlList: list[CutsceneCmdGiveTatlList] = field(default_factory=list)


class CutsceneObjectFactory:
    """This class contains functions to create new Blender objects"""

    def getNewObject(self, name: str, data, selectObject: bool, parentObj: Object) -> Object:
        newObj = bpy.data.objects.new(name=name, object_data=data)
        bpy.context.view_layer.active_layer_collection.collection.objects.link(newObj)
        if selectObject:
            newObj.select_set(True)
            bpy.context.view_layer.objects.active = newObj
        newObj.parent = parentObj
        newObj.location = [0.0, 0.0, 0.0]
        newObj.rotation_euler = [0.0, 0.0, 0.0]
        newObj.scale = [1.0, 1.0, 1.0]
        return newObj

    def getNewEmptyObject(self, name: str, selectObject: bool, parentObj: Object):
        return self.getNewObject(name, None, selectObject, parentObj)

    def getNewArmatureObject(self, name: str, selectObject: bool, parentObj: Object):
        newArmatureData = bpy.data.armatures.new(name)
        newArmatureData.display_type = "STICK"
        newArmatureData.show_names = True
        newArmatureObject = self.getNewObject(name, newArmatureData, selectObject, parentObj)
        return newArmatureObject

    def getNewCutsceneObject(self, name: str, frameCount: int, parentObj: Object):
        newCSObj = self.getNewEmptyObject(name, True, parentObj)
        newCSObj.ootEmptyType = "Cutscene"
        newCSObj.ootCutsceneProperty.csEndFrame = frameCount
        return newCSObj

    def getNewActorCueListObject(self, name: str, commandType: str, parentObj: Object):
        newActorCueListObj = self.getNewEmptyObject(name, False, parentObj)
        newActorCueListObj.ootEmptyType = f"CS {'Player' if 'Player' in name else 'Actor'} Cue List"
        cmdEnum = oot_data.enumData.enumByKey["csCmd"]

        if commandType == "Player":
            commandType = "player_cue"

        index = (
            cmdEnum.item_by_key[commandType].index if commandType in cmdEnum.item_by_key else int(commandType, base=16)
        )
        item = cmdEnum.item_by_index.get(index)

        if item is not None:
            newActorCueListObj.ootCSMotionProperty.actorCueListProp.commandType = item.key
        else:
            newActorCueListObj.ootCSMotionProperty.actorCueListProp.commandType = "Custom"
            newActorCueListObj.ootCSMotionProperty.actorCueListProp.commandTypeCustom = commandType

        return newActorCueListObj

    def getNewActorCueObject(
        self,
        name: str,
        startFrame: int,
        actionID: int | str,
        location: list[int],
        rot: list[str],
        parentObj: Object,
    ):
        isDummy = "(D)" in name
        isPlayer = not isDummy and not "Actor" in name

        newActorCueObj = self.getNewEmptyObject(name, False, parentObj)
        newActorCueObj.location = getBlenderPosition(location, bpy.context.scene.ootBlenderScale)
        newActorCueObj.empty_display_type = "ARROWS"
        newActorCueObj.rotation_mode = "XZY"
        newActorCueObj.rotation_euler = getBlenderRotation(rot)
        emptyType = "Dummy" if isDummy else "Player" if isPlayer else "Actor"
        newActorCueObj.ootEmptyType = f"CS {emptyType} Cue"
        newActorCueObj.ootCSMotionProperty.actorCueProp.cueStartFrame = startFrame

        item = None
        if isPlayer:
            playerEnum = oot_data.enumData.enumByKey["csPlayerCueId"]
            if isinstance(actionID, int):
                item = playerEnum.item_by_index.get(actionID)
            else:
                item = playerEnum.item_by_key.get(actionID)

        if item is not None:
            newActorCueObj.ootCSMotionProperty.actorCueProp.playerCueID = item.key
        elif not isDummy:
            if isPlayer:
                newActorCueObj.ootCSMotionProperty.actorCueProp.playerCueID = "Custom"

            if isinstance(actionID, int):
                cueActionID = f"0x{actionID:04X}"
            else:
                cueActionID = actionID

            newActorCueObj.ootCSMotionProperty.actorCueProp.cueActionID = cueActionID

        return newActorCueObj

    def getNewCameraObject(
        self, name: str, displaySize: float, clipStart: float, clipEnd: float, alpha: float, parentObj: Object
    ):
        newCamera = bpy.data.cameras.new(name)
        newCameraObj = self.getNewObject(name, newCamera, False, parentObj)
        newCameraObj.data.display_size = displaySize
        newCameraObj.data.clip_start = clipStart
        newCameraObj.data.clip_end = clipEnd
        newCameraObj.data.passepartout_alpha = alpha
        return newCameraObj

    def getNewActorCuePreviewObject(self, name: str, selectObject, parentObj: Object):
        newPreviewObj = self.getNewEmptyObject(name, selectObject, parentObj)
        newPreviewObj.ootEmptyType = f"CS {'Actor' if 'Actor' in name else 'Player'} Cue Preview"
        return newPreviewObj
