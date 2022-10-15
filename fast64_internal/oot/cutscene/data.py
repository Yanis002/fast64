ootEnumCSListType = [
    ("Textbox", "Textbox", "Textbox"),
    ("FX", "Transition", "Transition"),
    ("Lighting", "Lighting", "Lighting"),
    ("Time", "Time", "Time"),
    ("PlayBGM", "Play BGM", "Play BGM"),
    ("StopBGM", "Stop BGM", "Stop BGM"),
    ("FadeBGM", "Fade BGM", "Fade BGM"),
    ("Misc", "Misc", "Misc"),
    ("0x09", "Rumble Controller", "Rumble Controller"),
    ("Unk", "Unknown Data", "Unknown Data"),
]

ootEnumCSListTypeIcons = [
    "ALIGN_BOTTOM",
    "COLORSET_10_VEC",
    "LIGHT_SUN",
    "TIME",
    "PLAY",
    "SNAP_FACE",
    "IPO_EASE_IN_OUT",
    "OPTIONS",
    "EVENT_F9",
    "QUESTION",
]

ootEnumCSTextboxType = [("Text", "Text", "Text"), ("None", "None", "None"), ("LearnSong", "Learn Song", "Learn Song")]

ootEnumCSTextboxTypeIcons = ["FILE_TEXT", "HIDE_ON", "FILE_SOUND"]

ootEnumCSTransitionType = [
    ("1", "White Fill +", "Has hardcoded sounds for some scenes"),
    ("2", "Blue Fill", "Blue Fill"),
    ("3", "Red Fill", "Red Fill"),
    ("4", "Green Fill", "Green Fill"),
    ("5", "White Unfill", "White Unfill"),
    ("6", "Blue Unfill", "Blue Unfill"),
    ("7", "Red Unfill", "Red Unfill"),
    ("8", "Green Unfill", "Green Unfill"),
    (
        "9",
        "White Trigger Unfill",
        "The screen will stay white until the command starts",
    ),  # TRANS_TYPE_FADE_WHITE_CS_DELAYED
    ("10", "Black Fill", "Black Fill"),
    ("11", "Black Unfill", "Black Unfill"),
    ("12", "Black Half Fill", "Black Half Fill"),  # TRANS_TYPE_CS_BLACK_FILL
    ("13", "Black Half Unfill", "Black Half Unfill"),  # 12 and 13 inverted?
]
