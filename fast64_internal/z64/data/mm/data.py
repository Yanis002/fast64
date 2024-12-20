from dataclasses import dataclass


@dataclass
class MM_BaseElement:
    id: str
    key: str
    name: str
    index: int


@dataclass
class MM_Data:
    """Contains data related to MM, like actors or objects"""

    def __init__(self):
        from .enum_data import MM_EnumData
        from .actor_data import MM_ActorData

        self.enum_data = MM_EnumData()
        self.actor_data = MM_ActorData()

        self.enum_seq_id = [
            ("Custom", "Custom", "Custom"),
            ("NA_BGM_GENERAL_SFX", "General Sound Effects", "General Sound Effects"),
            ("NA_BGM_AMBIENCE", "Ambient background noises", "Ambient background noises"),
            ("NA_BGM_TERMINA_FIELD", "Termina Field", "Termina Field"),
            ("NA_BGM_CHASE", "Chase", "Chase"),
            ("NA_BGM_MAJORAS_THEME", "Majora's Theme", "Majora's Theme"),
            ("NA_BGM_CLOCK_TOWER", "Clock Tower", "Clock Tower"),
            ("NA_BGM_STONE_TOWER_TEMPLE", "Stone Tower Temple", "Stone Tower Temple"),
            ("NA_BGM_INV_STONE_TOWER_TEMPLE", "Stone Tower Temple Upside-down", "Stone Tower Temple Upside-down"),
            ("NA_BGM_FAILURE_0", "Missed Event 1", "Missed Event 1"),
            ("NA_BGM_FAILURE_1", "Missed Event 2", "Missed Event 2"),
            ("NA_BGM_HAPPY_MASK_SALESMAN", "Happy Mask Saleman's Theme", "Happy Mask Saleman's Theme"),
            ("NA_BGM_SONG_OF_HEALING", "Song Of Healing", "Song Of Healing"),
            ("NA_BGM_SWAMP_REGION", "Southern Swamp", "Southern Swamp"),
            ("NA_BGM_ALIEN_INVASION", "Ghost Attack", "Ghost Attack"),
            ("NA_BGM_SWAMP_CRUISE", "Boat Cruise", "Boat Cruise"),
            ("NA_BGM_SHARPS_CURSE", "Sharp's Curse", "Sharp's Curse"),
            ("NA_BGM_GREAT_BAY_REGION", "Great Bay Coast", "Great Bay Coast"),
            ("NA_BGM_IKANA_REGION", "Ikana Valley", "Ikana Valley"),
            ("NA_BGM_DEKU_PALACE", "Deku Palace", "Deku Palace"),
            ("NA_BGM_MOUNTAIN_REGION", "Mountain Village", "Mountain Village"),
            ("NA_BGM_PIRATES_FORTRESS", "Pirates' Fortress", "Pirates' Fortress"),
            ("NA_BGM_CLOCK_TOWN_DAY_1", "Clock Town, First Day", "Clock Town, First Day"),
            ("NA_BGM_CLOCK_TOWN_DAY_2", "Clock Town, Second Day", "Clock Town, Second Day"),
            ("NA_BGM_CLOCK_TOWN_DAY_3", "Clock Town, Third Day", "Clock Town, Third Day"),
            ("NA_BGM_FILE_SELECT", "File Select", "File Select"),
            ("NA_BGM_CLEAR_EVENT", "Event Clear", "Event Clear"),
            ("NA_BGM_ENEMY", "Battle", "Battle"),
            ("NA_BGM_BOSS", "Boss Battle", "Boss Battle"),
            ("NA_BGM_WOODFALL_TEMPLE", "Woodfall Temple", "Woodfall Temple"),
            ("NA_BGM_CLOCK_TOWN_MAIN_SEQUENCE", "NA_BGM_CLOCK_TOWN_MAIN_SEQUENCE", "NA_BGM_CLOCK_TOWN_MAIN_SEQUENCE"),
            ("NA_BGM_OPENING", "Opening", "Opening"),
            ("NA_BGM_INSIDE_A_HOUSE", "House", "House"),
            ("NA_BGM_GAME_OVER", "Game Over", "Game Over"),
            ("NA_BGM_CLEAR_BOSS", "Boss Clear", "Boss Clear"),
            ("NA_BGM_GET_ITEM", "Item Catch", "Item Catch"),
            ("NA_BGM_CLOCK_TOWN_DAY_2_PTR", "NA_BGM_CLOCK_TOWN_DAY_2_PTR", "NA_BGM_CLOCK_TOWN_DAY_2_PTR"),
            ("NA_BGM_GET_HEART", "Get A Heart Container", "Get A Heart Container"),
            ("NA_BGM_TIMED_MINI_GAME", "Mini Game", "Mini Game"),
            ("NA_BGM_GORON_RACE", "Goron Race", "Goron Race"),
            ("NA_BGM_MUSIC_BOX_HOUSE", "Music Box House", "Music Box House"),
            ("NA_BGM_FAIRY_FOUNTAIN", "Fairy's Fountain", "Fairy's Fountain"),
            ("NA_BGM_ZELDAS_LULLABY", "Zelda's Theme", "Zelda's Theme"),
            ("NA_BGM_ROSA_SISTERS", "Rosa Sisters", "Rosa Sisters"),
            ("NA_BGM_OPEN_CHEST", "Open Treasure Box", "Open Treasure Box"),
            ("NA_BGM_MARINE_RESEARCH_LAB", "Marine Research Laboratory", "Marine Research Laboratory"),
            ("NA_BGM_GIANTS_THEME", "Giants' Theme", "Giants' Theme"),
            ("NA_BGM_SONG_OF_STORMS", "Guru-Guru's Song", "Guru-Guru's Song"),
            ("NA_BGM_ROMANI_RANCH", "Romani Ranch", "Romani Ranch"),
            ("NA_BGM_GORON_VILLAGE", "Goron Village", "Goron Village"),
            ("NA_BGM_MAYORS_OFFICE", "Mayor's Meeting", "Mayor's Meeting"),
            ("NA_BGM_OCARINA_EPONA", "Ocarina “Epona's Song”", "Ocarina “Epona's Song”"),
            ("NA_BGM_OCARINA_SUNS", "Ocarina “Sun's Song”", "Ocarina “Sun's Song”"),
            ("NA_BGM_OCARINA_TIME", "Ocarina “Song Of Time”", "Ocarina “Song Of Time”"),
            ("NA_BGM_OCARINA_STORM", "Ocarina “Song Of Storms”", "Ocarina “Song Of Storms”"),
            ("NA_BGM_ZORA_HALL", "Zora Hall", "Zora Hall"),
            ("NA_BGM_GET_NEW_MASK", "Get A Mask", "Get A Mask"),
            ("NA_BGM_MINI_BOSS", "Middle Boss Battle", "Middle Boss Battle"),
            ("NA_BGM_GET_SMALL_ITEM", "Small Item Catch", "Small Item Catch"),
            ("NA_BGM_ASTRAL_OBSERVATORY", "Astral Observatory", "Astral Observatory"),
            ("NA_BGM_CAVERN", "Cavern", "Cavern"),
            ("NA_BGM_MILK_BAR", "Milk Bar", "Milk Bar"),
            ("NA_BGM_ZELDA_APPEAR", "Enter Zelda", "Enter Zelda"),
            ("NA_BGM_SARIAS_SONG", "Woods Of Mystery", "Woods Of Mystery"),
            ("NA_BGM_GORON_GOAL", "Goron Race Goal", "Goron Race Goal"),
            ("NA_BGM_HORSE", "Horse Race", "Horse Race"),
            ("NA_BGM_HORSE_GOAL", "Horse Race Goal", "Horse Race Goal"),
            ("NA_BGM_INGO", "Gorman Track", "Gorman Track"),
            ("NA_BGM_KOTAKE_POTION_SHOP", "Magic Hags' Potion Shop", "Magic Hags' Potion Shop"),
            ("NA_BGM_SHOP", "Shop", "Shop"),
            ("NA_BGM_OWL", "Owl", "Owl"),
            ("NA_BGM_SHOOTING_GALLERY", "Shooting Gallery", "Shooting Gallery"),
            ("NA_BGM_OCARINA_SOARING", "Ocarina “Song Of Soaring”", "Ocarina “Song Of Soaring”"),
            ("NA_BGM_OCARINA_HEALING", "Ocarina “Song Of Healing”", "Ocarina “Song Of Healing”"),
            ("NA_BGM_INVERTED_SONG_OF_TIME", "Ocarina “Inverted Song Of Time”", "Ocarina “Inverted Song Of Time”"),
            ("NA_BGM_SONG_OF_DOUBLE_TIME", "Ocarina “Song Of Double Time”", "Ocarina “Song Of Double Time”"),
            ("NA_BGM_SONATA_OF_AWAKENING", "Sonata of Awakening", "Sonata of Awakening"),
            ("NA_BGM_GORON_LULLABY", "Goron Lullaby", "Goron Lullaby"),
            ("NA_BGM_NEW_WAVE_BOSSA_NOVA", "New Wave Bossa Nova", "New Wave Bossa Nova"),
            ("NA_BGM_ELEGY_OF_EMPTINESS", "Elegy Of Emptiness", "Elegy Of Emptiness"),
            ("NA_BGM_OATH_TO_ORDER", "Oath To Order", "Oath To Order"),
            ("NA_BGM_SWORD_TRAINING_HALL", "Swordsman's School", "Swordsman's School"),
            ("NA_BGM_OCARINA_LULLABY_INTRO", "Ocarina “Goron Lullaby Intro”", "Ocarina “Goron Lullaby Intro”"),
            ("NA_BGM_LEARNED_NEW_SONG", "Get The Ocarina", "Get The Ocarina"),
            ("NA_BGM_BREMEN_MARCH", "Bremen March", "Bremen March"),
            ("NA_BGM_BALLAD_OF_THE_WIND_FISH", "Ballad Of The Wind Fish", "Ballad Of The Wind Fish"),
            ("NA_BGM_SONG_OF_SOARING", "Song Of Soaring", "Song Of Soaring"),
            ("NA_BGM_MILK_BAR_DUPLICATE", "NA_BGM_MILK_BAR_DUPLICATE", "NA_BGM_MILK_BAR_DUPLICATE"),
            ("NA_BGM_FINAL_HOURS", "Last Day", "Last Day"),
            ("NA_BGM_MIKAU_RIFF", "Mikau", "Mikau"),
            ("NA_BGM_MIKAU_FINALE", "Mikau", "Mikau"),
            ("NA_BGM_FROG_SONG", "Frog Song", "Frog Song"),
            ("NA_BGM_OCARINA_SONATA", "Ocarina “Sonata Of Awakening”", "Ocarina “Sonata Of Awakening”"),
            ("NA_BGM_OCARINA_LULLABY", "Ocarina “Goron Lullaby”", "Ocarina “Goron Lullaby”"),
            ("NA_BGM_OCARINA_NEW_WAVE", "Ocarina “New Wave Bossa Nova”", "Ocarina “New Wave Bossa Nova”"),
            ("NA_BGM_OCARINA_ELEGY", "Ocarina “Elegy of Emptiness”", "Ocarina “Elegy of Emptiness”"),
            ("NA_BGM_OCARINA_OATH", "Ocarina “Oath To Order”", "Ocarina “Oath To Order”"),
            ("NA_BGM_MAJORAS_LAIR", "Majora Boss Room", "Majora Boss Room"),
            ("NA_BGM_OCARINA_LULLABY_INTRO_PTR", "NA_BGM_OCARINA_LULLABY_INTRO", "NA_BGM_OCARINA_LULLABY_INTRO"),
            ("NA_BGM_OCARINA_GUITAR_BASS_SESSION", "Bass and Guitar Session", "Bass and Guitar Session"),
            ("NA_BGM_PIANO_SESSION", "Piano Solo", "Piano Solo"),
            ("NA_BGM_INDIGO_GO_SESSION", "The Indigo-Go's", "The Indigo-Go's"),
            ("NA_BGM_SNOWHEAD_TEMPLE", "Snowhead Temple", "Snowhead Temple"),
            ("NA_BGM_GREAT_BAY_TEMPLE", "Great Bay Temple", "Great Bay Temple"),
            ("NA_BGM_NEW_WAVE_SAXOPHONE", "New Wave Bossa Nova", "New Wave Bossa Nova"),
            ("NA_BGM_NEW_WAVE_VOCAL", "New Wave Bossa Nova", "New Wave Bossa Nova"),
            ("NA_BGM_MAJORAS_WRATH", "Majora's Wrath Battle", "Majora's Wrath Battle"),
            ("NA_BGM_MAJORAS_INCARNATION", "Majora's Incarnate Battle", "Majora's Incarnate Battle"),
            ("NA_BGM_MAJORAS_MASK", "Majora's Mask Battle", "Majora's Mask Battle"),
            ("NA_BGM_BASS_PLAY", "Bass Practice", "Bass Practice"),
            ("NA_BGM_DRUMS_PLAY", "Drums Practice", "Drums Practice"),
            ("NA_BGM_PIANO_PLAY", "Piano Practice", "Piano Practice"),
            ("NA_BGM_IKANA_CASTLE", "Ikana Castle", "Ikana Castle"),
            ("NA_BGM_GATHERING_GIANTS", "Calling The Four Giants", "Calling The Four Giants"),
            ("NA_BGM_KAMARO_DANCE", "Kamaro's Dance", "Kamaro's Dance"),
            ("NA_BGM_CREMIA_CARRIAGE", "Cremia's Carriage", "Cremia's Carriage"),
            ("NA_BGM_KEATON_QUIZ", "Keaton's Quiz", "Keaton's Quiz"),
            ("NA_BGM_END_CREDITS", "The End / Credits", "The End / Credits"),
            ("NA_BGM_OPENING_LOOP", "NA_BGM_OPENING_LOOP", "NA_BGM_OPENING_LOOP"),
            ("NA_BGM_TITLE_THEME", "Title Theme", "Title Theme"),
            ("NA_BGM_DUNGEON_APPEAR", "Woodfall Rises", "Woodfall Rises"),
            ("NA_BGM_WOODFALL_CLEAR", "Southern Swamp Clears", "Southern Swamp Clears"),
            ("NA_BGM_SNOWHEAD_CLEAR", "Snowhead Clear", "Snowhead Clear"),
            ("NA_BGM_INTO_THE_MOON", "To The Moon", "To The Moon"),
            ("NA_BGM_GOODBYE_GIANT", "The Giants' Exit", "The Giants' Exit"),
            ("NA_BGM_TATL_AND_TAEL", "Tatl and Tael", "Tatl and Tael"),
            ("NA_BGM_MOONS_DESTRUCTION", "Moon's Destruction", "Moon's Destruction"),
            ("NA_BGM_END_CREDITS_SECOND_HALF", "The End / Credits (Half 2)", "The End / Credits (Half 2)"),
        ]

        self.enum_ambiance_id = [
            ("Custom", "Custom", "Custom"),
            ("0x00", "AMBIENCE_ID_00", "AMBIENCE_ID_00"),
            ("0x01", "AMBIENCE_ID_01", "AMBIENCE_ID_01"),
            ("0x02", "AMBIENCE_ID_02", "AMBIENCE_ID_02"),
            ("0x03", "AMBIENCE_ID_03", "AMBIENCE_ID_03"),
            ("0x04", "AMBIENCE_ID_04", "AMBIENCE_ID_04"),
            ("0x05", "AMBIENCE_ID_05", "AMBIENCE_ID_05"),
            ("0x06", "AMBIENCE_ID_06", "AMBIENCE_ID_06"),
            ("0x07", "AMBIENCE_ID_07", "AMBIENCE_ID_07"),
            ("0x08", "AMBIENCE_ID_08", "AMBIENCE_ID_08"),
            ("0x09", "AMBIENCE_ID_09", "AMBIENCE_ID_09"),
            ("0x0A", "AMBIENCE_ID_0A", "AMBIENCE_ID_0A"),
            ("0x0B", "AMBIENCE_ID_0B", "AMBIENCE_ID_0B"),
            ("0x0C", "AMBIENCE_ID_0C", "AMBIENCE_ID_0C"),
            ("0x0D", "AMBIENCE_ID_0D", "AMBIENCE_ID_0D"),
            ("0x0E", "AMBIENCE_ID_0E", "AMBIENCE_ID_0E"),
            ("0x0F", "AMBIENCE_ID_0F", "AMBIENCE_ID_0F"),
            ("0x10", "AMBIENCE_ID_10", "AMBIENCE_ID_10"),
            ("0x11", "AMBIENCE_ID_11", "AMBIENCE_ID_11"),
            ("0x12", "AMBIENCE_ID_12", "AMBIENCE_ID_12"),
            ("0x13", "AMBIENCE_ID_13", "AMBIENCE_ID_13"),
            ("0xFF", "AMBIENCE_ID_DISABLED", "AMBIENCE_ID_DISABLED"),
        ]
