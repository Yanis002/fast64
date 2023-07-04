ootEnumCSMotionCamMode = [
    ("splineEyeOrAT", "Normal", "Normal (0x1 / 0x2)"),
    ("splineEyeOrATRelPlayer", "Rel. Link", "Relative to Link (0x5 / 0x6)"),
    ("eyeOrAT", "0x7/0x8", "Not Yet Understood Mode (0x7 / 0x8)"),  # remove?
]

# Default width is 16

CAM_LIST_PARAMS = [
    {"name": "continueFlag", "type": "continueFlag"},
    {"name": "roll", "type": "int", "width": 8},
    {"name": "frame", "type": "int"},
    {"name": "viewAngle", "type": "int_or_float", "min": 0.0, "max": 179.99},
    {"name": "xPos", "type": "int"},
    {"name": "yPos", "type": "int"},
    {"name": "zPos", "type": "int"},
    {"name": "unused", "type": "int"},
]

ACTOR_ACTION_PARAMS = [
    {"name": "action", "type": "string"},
    {"name": "startFrame", "type": "int"},
    {"name": "endFrame", "type": "int"},
    {"name": "rotX", "type": "hex"},
    {"name": "rotY", "type": "hex"},
    {"name": "rotZ", "type": "hex"},
    {"name": "startX", "type": "int", "width": 32},
    {"name": "startY", "type": "int", "width": 32},
    {"name": "startZ", "type": "int", "width": 32},
    {"name": "endX", "type": "int", "width": 32},
    {"name": "endY", "type": "int", "width": 32},
    {"name": "endZ", "type": "int", "width": 32},
    {"name": "normX", "type": "int_or_float", "width": 32},
    {"name": "normY", "type": "int_or_float", "width": 32},
    {"name": "normZ", "type": "int_or_float", "width": 32},
]

BGM_PARAMS = [
    {"name": "id", "type": "string"},
    {"name": "startFrame", "type": "int"},
    {"name": "endFrame", "type": "int"},
    {"name": "unused0", "type": "int"},
    {"name": "unused1", "type": "int", "width": 32},
    {"name": "unused2", "type": "int", "width": 32},
    {"name": "unused3", "type": "int", "width": 32},
    {"name": "unused4", "type": "int", "width": 32},
    {"name": "unused5", "type": "int", "width": 32},
    {"name": "unused6", "type": "int", "width": 32},
    {"name": "unused7", "type": "int", "width": 32},
]

CAM_TYPE_LISTS = [
    "CS_CAM_POS_LIST",
    "CS_CAM_FOCUS_POINT_LIST",
    "CS_CAM_POS_PLAYER_LIST",
    "CS_CAM_FOCUS_POINT_PLAYER_LIST",
    "CS_CMD_07_LIST",
    "CS_CMD_08_LIST",
]

CAM_TYPE_TO_TYPE = {
    "CS_CAM_POS_LIST": "pos",
    "CS_CAM_FOCUS_POINT_LIST": "at",
    "CS_CAM_POS_PLAYER_LIST": "pos",
    "CS_CAM_FOCUS_POINT_PLAYER_LIST": "at",
    "CS_CMD_07_LIST": "pos",
    "CS_CMD_08_LIST": "at",
}

CAM_TYPE_TO_MODE = {
    "CS_CAM_POS_LIST": "splineEyeOrAT",
    "CS_CAM_FOCUS_POINT_LIST": "splineEyeOrAT",
    "CS_CAM_POS_PLAYER_LIST": "splineEyeOrATRelPlayer",
    "CS_CAM_FOCUS_POINT_PLAYER_LIST": "splineEyeOrATRelPlayer",
    "CS_CMD_07_LIST": "eyeOrAT",
    "CS_CMD_08_LIST": "eyeOrAT",
}

ATMODE_TO_CMD = {
    False: {"splineEyeOrAT": "CS_CAM_POS", "splineEyeOrATRelPlayer": "CS_CAM_POS_PLAYER", "eyeOrAT": "CS_CMD_07"},
    True: {
        "splineEyeOrAT": "CS_CAM_FOCUS_POINT",
        "splineEyeOrATRelPlayer": "CS_CAM_FOCUS_POINT_PLAYER",
        "eyeOrAT": "CS_CMD_08",
    },
}

ACTION_LISTS = ["CS_PLAYER_ACTION_LIST", "CS_NPC_ACTION_LIST"]

LISTS_DEF = [
    {
        "name": "CS_CAM_POS_LIST",
        "params": [{"name": "startFrame", "type": "int"}, {"name": "endFrame", "type": "int"}],
        "commands": [{"name": "CS_CAM_POS", "params": CAM_LIST_PARAMS}],
    },
    {
        "name": "CS_CAM_FOCUS_POINT_LIST",
        "params": [{"name": "startFrame", "type": "int"}, {"name": "endFrame", "type": "int"}],
        "commands": [{"name": "CS_CAM_FOCUS_POINT", "params": CAM_LIST_PARAMS}],
    },
    {
        "name": "CS_MISC_LIST",
        "params": [{"name": "entries", "type": "int", "min": 1}],
        "commands": [
            {
                "name": "CS_MISC",
                "params": [
                    {"name": "unk", "type": "hex"},
                    {"name": "startFrame", "type": "int"},
                    {"name": "endFrame", "type": "int"},
                    {"name": "unused0", "type": "hex"},
                    {"name": "unused1", "type": "hex", "width": 32},
                    {"name": "unused2", "type": "hex", "width": 32},
                    {"name": "unused3", "type": "int", "width": 32},
                    {"name": "unused4", "type": "int", "width": 32},
                    {"name": "unused5", "type": "int", "width": 32},
                    {"name": "unused6", "type": "int", "width": 32},
                    {"name": "unused7", "type": "int", "width": 32},
                    {"name": "unused8", "type": "int", "width": 32},
                    {"name": "unused9", "type": "int", "width": 32},
                    {"name": "unused10", "type": "int", "width": 32},
                ],
            }
        ],
    },
    {
        "name": "CS_LIGHTING_LIST",
        "params": [{"name": "entries", "type": "int", "min": 1}],
        "commands": [
            {
                "name": "CS_LIGHTING",
                "params": [
                    {"name": "setting", "type": "int"},
                    {"name": "startFrame", "type": "int"},
                    {"name": "endFrame", "type": "int"},
                    {"name": "unused0", "type": "int"},
                    {"name": "unused1", "type": "int", "width": 32},
                    {"name": "unused2", "type": "int", "width": 32},
                    {"name": "unused3", "type": "int", "width": 32},
                    {"name": "unused4", "type": "int", "width": 32},
                    {"name": "unused5", "type": "int", "width": 32},
                    {"name": "unused6", "type": "int", "width": 32},
                    {"name": "unused7", "type": "int", "width": 32},
                ],
            }
        ],
    },
    {
        "name": "CS_CAM_POS_PLAYER_LIST",
        "params": [{"name": "startFrame", "type": "int"}, {"name": "endFrame", "type": "int"}],
        "commands": [{"name": "CS_CAM_POS_PLAYER", "params": CAM_LIST_PARAMS}],
    },
    {
        "name": "CS_CAM_FOCUS_POINT_PLAYER_LIST",
        "params": [{"name": "startFrame", "type": "int"}, {"name": "endFrame", "type": "int"}],
        "commands": [{"name": "CS_CAM_FOCUS_POINT_PLAYER", "params": CAM_LIST_PARAMS}],
    },
    {
        "name": "CS_CMD_07_LIST",
        "params": [
            {"name": "unk", "type": "hex"},
            {"name": "startFrame", "type": "int"},
            {"name": "endFrame", "type": "int"},
            {"name": "unused", "type": "hex"},
        ],
        "commands": [{"name": "CS_CMD_07", "params": CAM_LIST_PARAMS}],
    },
    {
        "name": "CS_CMD_08_LIST",
        "params": [
            {"name": "unk", "type": "hex"},
            {"name": "startFrame", "type": "int"},
            {"name": "endFrame", "type": "int"},
            {"name": "unused", "type": "hex"},
        ],
        "commands": [{"name": "CS_CMD_08", "params": CAM_LIST_PARAMS}],
    },
    {
        "name": "CS_CMD_09_LIST",
        "params": [{"name": "entries", "type": "int", "min": 1}],
        "commands": [
            {
                "name": "CS_CMD_09",
                "params": [
                    {"name": "unk", "type": "int"},
                    {"name": "startFrame", "type": "int"},
                    {"name": "endFrame", "type": "int"},
                    {"name": "unk2", "type": "int", "width": 8},
                    {"name": "unk3", "type": "int", "width": 8},
                    {"name": "unk4", "type": "int", "width": 8},
                    {"name": "unused0", "type": "int", "width": 8},
                    {"name": "unused1", "type": "int"},
                ],
            }
        ],
    },
    {
        "name": "CS_UNK_DATA_LIST",
        "params": [{"name": "cmdType", "type": "int"}, {"name": "entries", "type": "int", "min": 1}],
        "commands": [
            {
                "name": "CS_UNK_DATA",
                "params": [
                    {"name": "unk1", "type": "int", "width": 32},
                    {"name": "unk2", "type": "int", "width": 32},
                    {"name": "unk3", "type": "int", "width": 32},
                    {"name": "unk4", "type": "int", "width": 32},
                    {"name": "unk5", "type": "int", "width": 32},
                    {"name": "unk6", "type": "int", "width": 32},
                    {"name": "unk7", "type": "int", "width": 32},
                    {"name": "unk8", "type": "int", "width": 32},
                    {"name": "unk9", "type": "int", "width": 32},
                    {"name": "unk10", "type": "int", "width": 32},
                    {"name": "unk11", "type": "int", "width": 32},
                    {"name": "unk12", "type": "int", "width": 32},
                ],
            }
        ],
    },
    {
        "name": "CS_NPC_ACTION_LIST",
        "params": [{"name": "cmdType", "type": "int"}, {"name": "entries", "type": "int", "min": 1}],
        "commands": [{"name": "CS_NPC_ACTION", "params": ACTOR_ACTION_PARAMS}],
    },
    {
        "name": "CS_PLAYER_ACTION_LIST",
        "params": [{"name": "entries", "type": "int", "min": 1}],
        "commands": [{"name": "CS_PLAYER_ACTION", "params": ACTOR_ACTION_PARAMS}],
    },
    {
        "name": "CS_TEXT_LIST",
        "params": [{"name": "entries", "type": "int", "min": 1}],
        "commands": [
            {
                "name": "CS_TEXT_DISPLAY_TEXTBOX",
                "params": [
                    {"name": "messageId", "type": "int"},
                    {"name": "startFrame", "type": "int"},
                    {"name": "endFrame", "type": "int"},
                    {"name": "type", "type": "int"},
                    {"name": "topOptionBranch", "type": "int"},
                    {"name": "bottomOptionBranch", "type": "int"},
                ],
            },
            {
                "name": "CS_TEXT_NONE",
                "params": [{"name": "startFrame", "type": "int"}, {"name": "endFrame", "type": "int"}],
            },
            {
                "name": "CS_TEXT_LEARN_SONG",
                "params": [
                    {"name": "ocarinaSongAction", "type": "int"},
                    {"name": "startFrame", "type": "int"},
                    {"name": "endFrame", "type": "int"},
                    {"name": "messageId", "type": "int"},
                ],
            },
        ],
    },
    {
        "name": "CS_PLAY_BGM_LIST",
        "params": [{"name": "entries", "type": "int", "min": 1}],
        "commands": [{"name": "CS_PLAY_BGM", "params": BGM_PARAMS}],
    },
    {
        "name": "CS_STOP_BGM_LIST",
        "params": [{"name": "entries", "type": "int", "min": 1}],
        "commands": [{"name": "CS_STOP_BGM", "params": BGM_PARAMS}],
    },
    {
        "name": "CS_FADE_BGM_LIST",
        "params": [{"name": "entries", "type": "int", "min": 1}],
        "commands": [{"name": "CS_FADE_BGM", "params": BGM_PARAMS}],
    },
    {
        "name": "CS_TIME_LIST",
        "params": [{"name": "entries", "type": "int", "min": 1}],
        "commands": [
            {
                "name": "CS_TIME",
                "params": [
                    {"name": "unk", "type": "int"},
                    {"name": "startFrame", "type": "int"},
                    {"name": "endFrame", "type": "int"},
                    {"name": "hour", "type": "int", "width": 8},
                    {"name": "min", "type": "int", "width": 8},
                    {"name": "unused", "type": "int", "width": 32},
                ],
            }
        ],
    },
]

NONLISTS_DEF = [
    {
        "name": "CS_BEGIN_CUTSCENE",
        "params": [
            {"name": "totalEntries", "type": "int", "min": 0},
            {"name": "endFrame", "type": "int", "min": 1},
        ],
    },
    {
        "name": "CS_SCENE_TRANS_FX",
        "params": [
            {"name": "transitionType", "type": "int"},
            {"name": "startFrame", "type": "int"},
            {"name": "endFrame", "type": "int"},
        ],
    },
    {
        "name": "CS_TERMINATOR",
        "params": [
            {"name": "dest", "type": "hex"},
            {"name": "startFrame", "type": "int"},
            {"name": "endFrame", "type": "int"},
        ],
    },
    {"name": "CS_END", "params": []},
]

# ---

ootEnumCSActorCueListCommandType = [
    ("Custom", "Custom", "Custom"),
    ("0x000F", "CS_CMD_ACTOR_CUE_0_0", ""),
    ("0x0011", "CS_CMD_ACTOR_CUE_0_1", ""),
    ("0x0012", "CS_CMD_ACTOR_CUE_0_2", ""),
    ("0x0017", "CS_CMD_ACTOR_CUE_0_3", ""),
    ("0x0022", "CS_CMD_ACTOR_CUE_0_4", ""),
    ("0x0027", "CS_CMD_ACTOR_CUE_0_5", ""),
    ("0x002E", "CS_CMD_ACTOR_CUE_0_6", ""),
    ("0x004C", "CS_CMD_ACTOR_CUE_0_7", ""),
    ("0x0055", "CS_CMD_ACTOR_CUE_0_8", ""),
    ("0x005D", "CS_CMD_ACTOR_CUE_0_9", ""),
    ("0x0069", "CS_CMD_ACTOR_CUE_0_10", ""),
    ("0x006B", "CS_CMD_ACTOR_CUE_0_11", ""),
    ("0x006E", "CS_CMD_ACTOR_CUE_0_12", ""),
    ("0x0077", "CS_CMD_ACTOR_CUE_0_13", ""),
    ("0x007B", "CS_CMD_ACTOR_CUE_0_14", ""),
    ("0x008A", "CS_CMD_ACTOR_CUE_0_15", ""),
    ("0x008B", "CS_CMD_ACTOR_CUE_0_16", ""),
    ("0x0090", "CS_CMD_ACTOR_CUE_0_17", ""),
    ("0x000E", "CS_CMD_ACTOR_CUE_1_0", ""),
    ("0x0010", "CS_CMD_ACTOR_CUE_1_1", ""),
    ("0x0018", "CS_CMD_ACTOR_CUE_1_2", ""),
    ("0x0023", "CS_CMD_ACTOR_CUE_1_3", ""),
    ("0x0028", "CS_CMD_ACTOR_CUE_1_4", ""),
    ("0x0030", "CS_CMD_ACTOR_CUE_1_5", ""),
    ("0x0040", "CS_CMD_ACTOR_CUE_1_6", ""),
    ("0x0044", "CS_CMD_ACTOR_CUE_1_7", ""),
    ("0x0046", "CS_CMD_ACTOR_CUE_1_8", ""),
    ("0x004E", "CS_CMD_ACTOR_CUE_1_9", ""),
    ("0x0050", "CS_CMD_ACTOR_CUE_1_10", ""),
    ("0x005E", "CS_CMD_ACTOR_CUE_1_11", ""),
    ("0x0074", "CS_CMD_ACTOR_CUE_1_12", ""),
    ("0x0076", "CS_CMD_ACTOR_CUE_1_13", ""),
    ("0x0078", "CS_CMD_ACTOR_CUE_1_14", ""),
    ("0x007D", "CS_CMD_ACTOR_CUE_1_15", ""),
    ("0x0083", "CS_CMD_ACTOR_CUE_1_16", ""),
    ("0x008D", "CS_CMD_ACTOR_CUE_1_17", ""),
    ("0x0019", "CS_CMD_ACTOR_CUE_2_0", ""),
    ("0x0024", "CS_CMD_ACTOR_CUE_2_1", ""),
    ("0x0029", "CS_CMD_ACTOR_CUE_2_2", ""),
    ("0x0032", "CS_CMD_ACTOR_CUE_2_3", ""),
    ("0x0043", "CS_CMD_ACTOR_CUE_2_4", ""),
    ("0x0045", "CS_CMD_ACTOR_CUE_2_5", ""),
    ("0x0048", "CS_CMD_ACTOR_CUE_2_6", ""),
    ("0x004A", "CS_CMD_ACTOR_CUE_2_7", ""),
    ("0x0051", "CS_CMD_ACTOR_CUE_2_8", ""),
    ("0x006A", "CS_CMD_ACTOR_CUE_2_9", ""),
    ("0x0075", "CS_CMD_ACTOR_CUE_2_10", ""),
    ("0x0079", "CS_CMD_ACTOR_CUE_2_11", ""),
    ("0x007E", "CS_CMD_ACTOR_CUE_2_12", ""),
    ("0x0084", "CS_CMD_ACTOR_CUE_2_13", ""),
    ("0x001D", "CS_CMD_ACTOR_CUE_3_0", ""),
    ("0x0025", "CS_CMD_ACTOR_CUE_3_1", ""),
    ("0x002A", "CS_CMD_ACTOR_CUE_3_2", ""),
    ("0x0033", "CS_CMD_ACTOR_CUE_3_3", ""),
    ("0x0035", "CS_CMD_ACTOR_CUE_3_4", ""),
    ("0x003F", "CS_CMD_ACTOR_CUE_3_5", ""),
    ("0x0041", "CS_CMD_ACTOR_CUE_3_6", ""),
    ("0x0042", "CS_CMD_ACTOR_CUE_3_7", ""),
    ("0x004B", "CS_CMD_ACTOR_CUE_3_8", ""),
    ("0x0052", "CS_CMD_ACTOR_CUE_3_9", ""),
    ("0x006C", "CS_CMD_ACTOR_CUE_3_10", ""),
    ("0x007F", "CS_CMD_ACTOR_CUE_3_11", ""),
    ("0x0085", "CS_CMD_ACTOR_CUE_3_12", ""),
    ("0x001E", "CS_CMD_ACTOR_CUE_4_0", ""),
    ("0x0026", "CS_CMD_ACTOR_CUE_4_1", ""),
    ("0x002B", "CS_CMD_ACTOR_CUE_4_2", ""),
    ("0x002F", "CS_CMD_ACTOR_CUE_4_3", ""),
    ("0x0036", "CS_CMD_ACTOR_CUE_4_4", ""),
    ("0x004F", "CS_CMD_ACTOR_CUE_4_5", ""),
    ("0x0053", "CS_CMD_ACTOR_CUE_4_6", ""),
    ("0x0080", "CS_CMD_ACTOR_CUE_4_7", ""),
    ("0x0087", "CS_CMD_ACTOR_CUE_4_8", ""),
    ("0x002C", "CS_CMD_ACTOR_CUE_5_0", ""),
    ("0x0037", "CS_CMD_ACTOR_CUE_5_1", ""),
    ("0x004D", "CS_CMD_ACTOR_CUE_5_2", ""),
    ("0x0054", "CS_CMD_ACTOR_CUE_5_3", ""),
    ("0x005A", "CS_CMD_ACTOR_CUE_5_4", ""),
    ("0x0081", "CS_CMD_ACTOR_CUE_5_5", ""),
    ("0x0088", "CS_CMD_ACTOR_CUE_5_6", ""),
    ("0x001F", "CS_CMD_ACTOR_CUE_6_0", ""),
    ("0x0034", "CS_CMD_ACTOR_CUE_6_1", ""),
    ("0x0039", "CS_CMD_ACTOR_CUE_6_2", ""),
    ("0x003A", "CS_CMD_ACTOR_CUE_6_3", ""),
    ("0x0058", "CS_CMD_ACTOR_CUE_6_4", ""),
    ("0x0073", "CS_CMD_ACTOR_CUE_6_5", ""),
    ("0x0082", "CS_CMD_ACTOR_CUE_6_6", ""),
    ("0x0089", "CS_CMD_ACTOR_CUE_6_7", ""),
    ("0x0031", "CS_CMD_ACTOR_CUE_7_0", ""),
    ("0x003C", "CS_CMD_ACTOR_CUE_7_1", ""),
    ("0x0059", "CS_CMD_ACTOR_CUE_7_2", ""),
    ("0x006F", "CS_CMD_ACTOR_CUE_7_3", ""),
    ("0x0072", "CS_CMD_ACTOR_CUE_7_4", ""),
    ("0x0086", "CS_CMD_ACTOR_CUE_7_5", ""),
    ("0x008E", "CS_CMD_ACTOR_CUE_7_6", ""),
    ("0x003E", "CS_CMD_ACTOR_CUE_8_0", ""),
    ("0x008F", "CS_CMD_ACTOR_CUE_9_0", ""),
]