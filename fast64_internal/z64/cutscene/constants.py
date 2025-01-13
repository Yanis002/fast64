from ...game_data import game_data
from .classes import (
    CutsceneCmdActorCueList,
    CutsceneCmdActorCue,
    CutsceneCmdCamEyeSpline,
    CutsceneCmdCamATSpline,
    CutsceneCmdCamEyeSplineRelToPlayer,
    CutsceneCmdCamATSplineRelToPlayer,
    CutsceneCmdCamEye,
    CutsceneCmdCamAT,
    CutsceneCmdCamPoint,
    CutsceneCmdMisc,
    CutsceneCmdMiscList,
    CutsceneCmdTransition,
    CutsceneCmdText,
    CutsceneCmdTextNone,
    CutsceneCmdTextOcarinaAction,
    CutsceneCmdTextList,
    CutsceneCmdLightSetting,
    CutsceneCmdLightSettingList,
    CutsceneCmdTime,
    CutsceneCmdTimeList,
    CutsceneCmdStartStopSeq,
    CutsceneCmdStartStopSeqList,
    CutsceneCmdFadeSeq,
    CutsceneCmdFadeSeqList,
    CutsceneCmdRumbleController,
    CutsceneCmdRumbleControllerList,
    CutsceneCmdDestination,
    CutsceneCmdCamSplineList,
    CutsceneCmdTransitionList,
    CutsceneCmdDestinationList,
    CutsceneCmdMotionBlurList,
    CutsceneCmdModifySeqList,
    CutsceneCmdChooseCreditsScenesList,
    CutsceneCmdTransitionGeneralList,
    CutsceneCmdGiveTatlList,
    CutsceneCmdCamSpline,
    CutsceneCmdNewCamPoint,
    CutsceneCmdCamMisc,
    CutsceneCmdTextGeneric,
    CutsceneCmdTextMask,
    CutsceneCmdMotionBlur,
    CutsceneCmdModifySeq,
    CutsceneCmdChooseCreditsScenes,
    CutsceneCmdTransitionGeneral,
    CutsceneCmdGiveTatl,
)


ootEnumCSWriteType = [
    ("Custom", "Custom", "Provide the name of a cutscene header variable", "", 0),
    ("Object", "Object", "Reference to Blender object representing cutscene", "", 2),
]

csListTypeToIcon = {
    "TextList": "ALIGN_BOTTOM",
    "Transition": "COLORSET_10_VEC",
    "LightSettingsList": "LIGHT_SUN",
    "TimeList": "TIME",
    "StartSeqList": "PLAY",
    "StopSeqList": "SNAP_FACE",
    "FadeOutSeqList": "IPO_EASE_IN_OUT",
    "MiscList": "OPTIONS",
    "RumbleList": "OUTLINER_OB_FORCE_FIELD",
    "MotionBlurList": "ONIONSKIN_ON",
    "ModifySeqList": "IPO_CONSTANT",
    "CreditsSceneList": "WORLD",
    "TransitionGeneralList": "COLORSET_06_VEC",
    "StartAmbienceList": "SNAP_FACE",
    "FadeOutAmbienceList": "IPO_EASE_IN_OUT",
}

ootEnumCSTextboxType = [
    ("Text", "Text", "Text"),
    ("None", "None", "None"),
    ("OcarinaAction", "Ocarina Action", "Learn Song"),
]

ootEnumCSTextboxTypeIcons = {
    "Text": "FILE_TEXT",
    "None": "HIDE_ON",
    "OcarinaAction": "FILE_SOUND",
    "Default": "FILE_TEXT",
    "Type1": "ALIGN_LEFT",
    "Type3": "ALIGN_CENTER",
    "BossesRemains": "GHOST_ENABLED",
    "AllNormalMasks": "RECOVER_LAST",
}

ootCSSubPropToName = {
    "startFrame": "Start Frame",
    "endFrame": "End Frame",
    # TextBox
    "textID": "Text ID",
    "ocarinaAction": "Ocarina Action",
    "csTextType": "Text Type",
    "topOptionTextID": "Text ID for Top Option",
    "bottomOptionTextID": "Text ID for Bottom Option",
    "ocarinaMessageId": "Ocarina Message ID",
    # Lighting
    "lightSettingsIndex": "Light Settings Index",
    # Time
    "hour": "Hour",
    "minute": "Minute",
    # Seq
    "csSeqID": "Seq ID",
    "csSeqPlayer": "Seq Player Type",
    # Misc
    "csMiscType": "Misc Type",
    # Rumble
    "rumbleSourceStrength": "Source Strength",
    "rumbleDuration": "Duration",
    "rumbleDecreaseRate": "Decrease Rate",
    "rumble_type": "Rumble Type",
    # Transition
    "transition_type": "Transition Type",
    # Motion Blur
    "blur_type": "Motion Blur Type",
    # Transition General
    "trans_general_type": "Transition Type",
    "trans_color": "Transition Color",
    # Choose Credits Scene
    "credits_scene_type": "Credits Scene Type",
    # Modify Seq
    "mod_seq_type": "Modify Seq Type",
    # Lists
    "TextList": "Text List",
    "TimeList": "Time List",
    "FadeOutSeqList": "Fade-Out Seq List",
    "Transition": "Transition List",
    "StartSeqList": "Start Seq List",
    "MiscList": "Misc List",
    "LightSettingsList": "Light Settings List",
    "StopSeqList": "Stop Seq List",
    "RumbleList": "Rumble List",
    "MotionBlurList": "Motion Blur List",
    "ModifySeqList": "Modify Seq List",
    "CreditsSceneList": "Choose Credits Scene List",
    "TransitionGeneralList": "Transition General List",
    "StartAmbienceList": "Start Ambience List",
    "FadeOutAmbienceList": "Fade-Out Ambience List",
}

ootEnumCSMotionCamMode = [
    ("splineEyeOrAT", "Eye/AT Spline", "Eye/AT Spline"),
    ("splineEyeOrATRelPlayer", "Spline Rel. Player", "Relative to Player's location/yaw"),
    ("eyeOrAT", "Eye/AT Point", "Single Eye/AT point (not recommended)"),
]

# Import/Export

ootCSLegacyToNewCmdNames = {
    "CS_CAM_POS_LIST": "CS_CAM_EYE_SPLINE",
    "CS_CAM_FOCUS_POINT_LIST": "CS_CAM_AT_SPLINE",
    "CS_CAM_POS_PLAYER_LIST": "CS_CAM_EYE_SPLINE_REL_TO_PLAYER",
    "CS_CAM_FOCUS_POINT_PLAYER_LIST": "CS_CAM_AT_SPLINE_REL_TO_PLAYER",
    "CS_NPC_ACTION_LIST": "CS_ACTOR_CUE_LIST",
    "CS_PLAYER_ACTION_LIST": "CS_PLAYER_CUE_LIST",
    "CS_CMD_07": "CS_CAM_EYE",
    "CS_CMD_08": "CS_CAM_AT",
    "CS_CAM_POS": "CS_CAM_POINT",
    "CS_CAM_FOCUS_POINT": "CS_CAM_POINT",
    "CS_CAM_POS_PLAYER": "CS_CAM_POINT",
    "CS_CAM_FOCUS_POINT_PLAYER": "CS_CAM_POINT",
    "CS_NPC_ACTION": "CS_ACTOR_CUE",
    "CS_PLAYER_ACTION": "CS_PLAYER_CUE",
    "CS_CMD_09_LIST": "CS_RUMBLE_CONTROLLER_LIST",
    "CS_CMD_09": "CS_RUMBLE_CONTROLLER",
    "CS_TEXT_DISPLAY_TEXTBOX": "CS_TEXT",
    "CS_TEXT_LEARN_SONG": "CS_TEXT_OCARINA_ACTION",
    "CS_SCENE_TRANS_FX": "CS_TRANSITION",
    "CS_FADE_BGM_LIST": "CS_FADE_OUT_SEQ_LIST",
    "CS_FADE_BGM": "CS_FADE_OUT_SEQ",
    "CS_TERMINATOR": "CS_DESTINATION",
    "CS_LIGHTING_LIST": "CS_LIGHT_SETTING_LIST",
    "CS_LIGHTING": "L_CS_LIGHT_SETTING",
    "CS_PLAY_BGM_LIST": "CS_START_SEQ_LIST",
    "CS_PLAY_BGM": "L_CS_START_SEQ",
    "CS_STOP_BGM_LIST": "CS_STOP_SEQ_LIST",
    "CS_STOP_BGM": "L_CS_STOP_SEQ",
    "CS_BEGIN_CUTSCENE": "CS_HEADER",
    "CS_END": "CS_END_OF_SCRIPT",
}

ootCSListCommands = [
    "CS_ACTOR_CUE_LIST",
    "CS_PLAYER_CUE_LIST",
    "CS_CAM_EYE_SPLINE",
    "CS_CAM_AT_SPLINE",
    "CS_CAM_EYE_SPLINE_REL_TO_PLAYER",
    "CS_CAM_AT_SPLINE_REL_TO_PLAYER",
    "CS_CAM_EYE",
    "CS_CAM_AT",
    "CS_MISC_LIST",
    "CS_LIGHT_SETTING_LIST",
    "CS_RUMBLE_CONTROLLER_LIST",
    "CS_TEXT_LIST",
    "CS_START_SEQ_LIST",
    "CS_STOP_SEQ_LIST",
    "CS_FADE_OUT_SEQ_LIST",
    "CS_TIME_LIST",
    "CS_UNK_DATA_LIST",
    "CS_PLAY_BGM_LIST",
    "CS_STOP_BGM_LIST",
    "CS_LIGHTING_LIST",
    # from new system
    "CS_CAM_SPLINE_LIST",
    "CS_TRANSITION_LIST",
    "CS_DESTINATION_LIST",
    "CS_MOTION_BLUR_LIST",
    "CS_MODIFY_SEQ_LIST",
    "CS_CHOOSE_CREDITS_SCENES_LIST",
    "CS_TRANSITION_GENERAL_LIST",
    "CS_GIVE_TATL_LIST",
]

ootCSListEntryCommands = [
    "CS_ACTOR_CUE",
    "CS_PLAYER_CUE",
    "CS_CAM_POINT",
    "CS_MISC",
    "CS_LIGHT_SETTING",
    "CS_RUMBLE_CONTROLLER",
    "CS_TEXT",
    "CS_TEXT_NONE",
    "CS_TEXT_OCARINA_ACTION",
    "CS_START_SEQ",
    "CS_STOP_SEQ",
    "CS_FADE_OUT_SEQ",
    "CS_TIME",
    "CS_UNK_DATA",
    "CS_PLAY_BGM",
    "CS_STOP_BGM",
    "CS_LIGHTING",
    # some old commands need to remove 1 to the first argument to stay accurate
    "L_CS_LIGHT_SETTING",
    "L_CS_START_SEQ",
    "L_CS_STOP_SEQ",
    # from new system
    "CS_CAM_POINT_NEW",
    "CS_CAM_MISC",
    "CS_CAM_END",
    "CS_CAM_SPLINE",  # technically a list but treating it as an entry
    "CS_TEXT_DEFAULT",
    "CS_TEXT_TYPE_1",
    "CS_TEXT_TYPE_3",
    "CS_TEXT_BOSSES_REMAINS",
    "CS_TEXT_ALL_NORMAL_MASKS",
    "CS_MOTION_BLUR",
    "CS_MODIFY_SEQ",
    "CS_CHOOSE_CREDITS_SCENES",
    "CS_TRANSITION_GENERAL",
    "CS_GIVE_TATL",
]

ootCSSingleCommands = [
    "CS_HEADER",
    "CS_END_OF_SCRIPT",
    # note: `CutsceneImport.correct_command_lists()` can move these ones in `ootCSListEntryCommands`
    "CS_TRANSITION",
    "CS_DESTINATION",
]


ootCSListAndSingleCommands = ootCSSingleCommands + ootCSListCommands
ootCSListAndSingleCommands.remove("CS_HEADER")
ootCutsceneCommandsC = ootCSSingleCommands + ootCSListCommands + ootCSListEntryCommands
