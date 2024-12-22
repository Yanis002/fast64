from .data import OoT_Data, MM_Data


oot_data = OoT_Data()
mm_data = MM_Data()

ootEnumRoomShapeType = [
    # ("Custom", "Custom", "Custom"),
    ("ROOM_SHAPE_TYPE_NORMAL", "Normal", "Normal"),
    ("ROOM_SHAPE_TYPE_IMAGE", "Image", "Image"),
    ("ROOM_SHAPE_TYPE_CULLABLE", "Cullable", "Cullable"),
    ("ROOM_SHAPE_TYPE_NONE", "None", "None"),
]

ootEnumHeaderMenu = [
    ("Child Night", "Child Night", "Child Night"),
    ("Adult Day", "Adult Day", "Adult Day"),
    ("Adult Night", "Adult Night", "Adult Night"),
    ("Cutscene", "Cutscene", "Cutscene"),
]
ootEnumHeaderMenuComplete = [
    ("Child Day", "Child Day", "Child Day"),
] + ootEnumHeaderMenu

ootEnumLinkIdle = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "Default", "Default"),
    ("0x01", "Sneezing", "Sneezing"),
    ("0x02", "Wiping Forehead", "Wiping Forehead"),
    ("0x04", "Yawning", "Yawning"),
    ("0x07", "Gasping For Breath", "Gasping For Breath"),
    ("0x09", "Brandish Sword", "Brandish Sword"),
    ("0x0A", "Adjust Tunic", "Adjust Tunic"),
    ("0xFF", "Hops On Epona", "Hops On Epona"),
]

mm_enum_environment_type = [
    ("Custom", "Custom", "Custom"),
    ("ROOM_ENV_DEFAULT", "Default", "0x00"),
    ("ROOM_ENV_COLD", "Cold", "0x01"),
    ("ROOM_ENV_WARM", "Warm", "0x02"),
    ("ROOM_ENV_HOT", "Hot", "0x03"),
    ("ROOM_ENV_UNK_STRETCH_1", "Unknown Stretch 1", "0x04"),
    ("ROOM_ENV_UNK_STRETCH_2", "Unknown Stretch 2", "0x05"),
    ("ROOM_ENV_UNK_STRETCH_3", "Unknown Stretch 3", "0x06"),
]

ootEnumCloudiness = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "Sunny", "Sunny"),
    ("0x01", "Cloudy", "Cloudy"),
]

mm_enum_skybox_config = [
    ("Custom", "Custom", "Custom"),
    ("SKYBOX_CONFIG_0", "SKYBOX_CONFIG_0", "0x00"),
    ("SKYBOX_CONFIG_1", "SKYBOX_CONFIG_1", "0x01"),
    ("SKYBOX_CONFIG_2", "SKYBOX_CONFIG_2", "0x02"),
    ("SKYBOX_CONFIG_3", "SKYBOX_CONFIG_3", "0x03"),
    ("SKYBOX_CONFIG_4", "SKYBOX_CONFIG_4", "0x04"),
    ("SKYBOX_CONFIG_5", "SKYBOX_CONFIG_5", "0x05"),
    ("SKYBOX_CONFIG_6", "SKYBOX_CONFIG_6", "0x06"),
    ("SKYBOX_CONFIG_7", "SKYBOX_CONFIG_7", "0x07"),
    ("SKYBOX_CONFIG_8", "SKYBOX_CONFIG_8", "0x08"),
    ("SKYBOX_CONFIG_9", "SKYBOX_CONFIG_9", "0x09"),
    ("SKYBOX_CONFIG_10", "SKYBOX_CONFIG_10", "0x0A"),
    ("SKYBOX_CONFIG_11", "SKYBOX_CONFIG_11", "0x0B"),
    ("SKYBOX_CONFIG_12", "SKYBOX_CONFIG_12", "0x0C"),
    ("SKYBOX_CONFIG_13", "SKYBOX_CONFIG_13", "0x0D"),
    ("SKYBOX_CONFIG_14", "SKYBOX_CONFIG_14", "0x0E"),
    ("SKYBOX_CONFIG_15", "SKYBOX_CONFIG_15", "0x0F"),
    ("SKYBOX_CONFIG_16", "SKYBOX_CONFIG_16", "0x10"),
    ("SKYBOX_CONFIG_17", "SKYBOX_CONFIG_17", "0x11"),
    ("SKYBOX_CONFIG_18", "SKYBOX_CONFIG_18", "0x12"),
    ("SKYBOX_CONFIG_19", "SKYBOX_CONFIG_19", "0x13"),
    ("SKYBOX_CONFIG_20", "SKYBOX_CONFIG_20", "0x14"),
    ("SKYBOX_CONFIG_21", "SKYBOX_CONFIG_21", "0x15"),
    ("SKYBOX_CONFIG_22", "SKYBOX_CONFIG_22", "0x16"),
    ("SKYBOX_CONFIG_23", "SKYBOX_CONFIG_23", "0x17"),
    ("SKYBOX_CONFIG_24", "SKYBOX_CONFIG_24", "0x18"),
    ("SKYBOX_CONFIG_25", "SKYBOX_CONFIG_25", "0x19"),
    ("SKYBOX_CONFIG_26", "SKYBOX_CONFIG_26", "0x1A"),
    ("SKYBOX_CONFIG_27", "SKYBOX_CONFIG_27", "0x1B"),
]

ootEnumCameraMode = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "Default", "Default"),
    ("0x10", "Two Views, No C-Up", "Two Views, No C-Up"),
    ("0x20", "Rotating Background, Bird's Eye C-Up", "Rotating Background, Bird's Eye C-Up"),
    ("0x30", "Fixed Background, No C-Up", "Fixed Background, No C-Up"),
    ("0x40", "Rotating Background, No C-Up", "Rotating Background, No C-Up"),
    ("0x50", "Shooting Gallery", "Shooting Gallery"),
]

ootEnumMapLocation = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "Hyrule Field", "Hyrule Field"),
    ("0x01", "Kakariko Village", "Kakariko Village"),
    ("0x02", "Graveyard", "Graveyard"),
    ("0x03", "Zora's River", "Zora's River"),
    ("0x04", "Kokiri Forest", "Kokiri Forest"),
    ("0x05", "Sacred Forest Meadow", "Sacred Forest Meadow"),
    ("0x06", "Lake Hylia", "Lake Hylia"),
    ("0x07", "Zora's Domain", "Zora's Domain"),
    ("0x08", "Zora's Fountain", "Zora's Fountain"),
    ("0x09", "Gerudo Valley", "Gerudo Valley"),
    ("0x0A", "Lost Woods", "Lost Woods"),
    ("0x0B", "Desert Colossus", "Desert Colossus"),
    ("0x0C", "Gerudo's Fortress", "Gerudo's Fortress"),
    ("0x0D", "Haunted Wasteland", "Haunted Wasteland"),
    ("0x0E", "Market", "Market"),
    ("0x0F", "Hyrule Castle", "Hyrule Castle"),
    ("0x10", "Death Mountain Trail", "Death Mountain Trail"),
    ("0x11", "Death Mountain Crater", "Death Mountain Crater"),
    ("0x12", "Goron City", "Goron City"),
    ("0x13", "Lon Lon Ranch", "Lon Lon Ranch"),
    ("0x14", "Dampe's Grave & Windmill", "Dampe's Grave & Windmill"),
    ("0x15", "Ganon's Castle", "Ganon's Castle"),
    ("0x16", "Grottos & Fairy Fountains", "Grottos & Fairy Fountains"),
]

ootEnumSkybox = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "None", "None"),
    ("0x01", "Standard Sky", "Standard Sky"),
    ("0x02", "Hylian Bazaar", "Hylian Bazaar"),
    ("0x03", "Brown Cloudy Sky", "Brown Cloudy Sky"),
    ("0x04", "Market Ruins", "Market Ruins"),
    ("0x05", "Black Cloudy Night", "Black Cloudy Night"),
    ("0x07", "Link's House", "Link's House"),
    ("0x09", "Market (Main Square, Day)", "Market (Main Square, Day)"),
    ("0x0A", "Market (Main Square, Night)", "Market (Main Square, Night)"),
    ("0x0B", "Happy Mask Shop", "Happy Mask Shop"),
    ("0x0C", "Know-It-All Brothers' House", "Know-It-All Brothers' House"),
    ("0x0E", "Kokiri Twins' House", "Kokiri Twins' House"),
    ("0x0F", "Stable", "Stable"),
    ("0x10", "Stew Lady's House", "Stew Lady's House"),
    ("0x11", "Kokiri Shop", "Kokiri Shop"),
    ("0x13", "Goron Shop", "Goron Shop"),
    ("0x14", "Zora Shop", "Zora Shop"),
    ("0x16", "Kakariko Potions Shop", "Kakariko Potions Shop"),
    ("0x17", "Hylian Potions Shop", "Hylian Potions Shop"),
    ("0x18", "Bomb Shop", "Bomb Shop"),
    ("0x1A", "Dog Lady's House", "Dog Lady's House"),
    ("0x1B", "Impa's House", "Impa's House"),
    ("0x1C", "Gerudo Tent", "Gerudo Tent"),
    ("0x1D", "Environment Color", "Environment Color"),
    ("0x20", "Mido's House", "Mido's House"),
    ("0x21", "Saria's House", "Saria's House"),
    ("0x22", "Dog Guy's House", "Dog Guy's House"),
]

mm_enum_skybox = [
    ("Custom", "Custom", "Custom"),
    ("SKYBOX_NONE", "None", "0x00"),
    ("SKYBOX_NORMAL_SKY", "Standard Sky", "0x01"),
    ("SKYBOX_2", "SKYBOX_2", "0x02"),
    ("SKYBOX_3", "SKYBOX_3", "0x03"),
    ("SKYBOX_CUTSCENE_MAP", "Cutscene Map", "0x05"),
]

ootEnumSkyboxLighting = [
    # see ``LightMode`` enum in ``z64environment.h``
    ("Custom", "Custom", "Custom"),
    ("LIGHT_MODE_TIME", "Time Of Day", "Time Of Day"),
    ("LIGHT_MODE_SETTINGS", "Indoor", "Indoor"),
]

ootEnumAudioSessionPreset = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "0x00", "0x00"),
]

ootEnumGlobalObject = [
    ("Custom", "Custom", "Custom"),
    ("OBJECT_INVALID", "None", "None"),
    ("OBJECT_GAMEPLAY_FIELD_KEEP", "Overworld", "gameplay_field_keep"),
    ("OBJECT_GAMEPLAY_DANGEON_KEEP", "Dungeon", "gameplay_dangeon_keep"),
]

mm_enum_global_object = [
    ("Custom", "Custom", "Custom"),
    ("GAMEPLAY_FIELD_KEEP", "Overworld", "gameplay_field_keep"),
    ("GAMEPLAY_DANGEON_KEEP", "Dungeon", "gameplay_dangeon_keep"),
]

ootEnumNaviHints = [
    ("Custom", "Custom", "Custom"),
    ("NAVI_QUEST_HINTS_NONE", "None", "None"),
    ("NAVI_QUEST_HINTS_OVERWORLD", "Overworld", "elf_message_field"),
    ("NAVI_QUEST_HINTS_DUNGEON", "Dungeon", "elf_message_ydan"),
]

# The order of this list matters (normal OoT scene order as defined by ``scene_table.h``)
ootEnumSceneID = [
    ("Custom", "Custom", "Custom"),
    ("SCENE_DEKU_TREE", "Inside the Deku Tree (Ydan)", "Ydan"),
    ("SCENE_DODONGOS_CAVERN", "Dodongo's Cavern (Ddan)", "Ddan"),
    ("SCENE_JABU_JABU", "Inside Jabu Jabu's Belly (Bdan)", "Bdan"),
    ("SCENE_FOREST_TEMPLE", "Forest Temple (Bmori1)", "Bmori1"),
    ("SCENE_FIRE_TEMPLE", "Fire Temple (Hidan)", "Hidan"),
    ("SCENE_WATER_TEMPLE", "Water Temple (Mizusin)", "Mizusin"),
    ("SCENE_SPIRIT_TEMPLE", "Spirit Temple (Jyasinzou)", "Jyasinzou"),
    ("SCENE_SHADOW_TEMPLE", "Shadow Temple (Hakadan)", "Hakadan"),
    ("SCENE_BOTTOM_OF_THE_WELL", "Bottom of the Well (Hakadanch)", "Hakadanch"),
    ("SCENE_ICE_CAVERN", "Ice Cavern (Ice Doukuto)", "Ice Doukuto"),
    ("SCENE_GANONS_TOWER", "Ganon's Tower (Ganon)", "Ganon"),
    ("SCENE_GERUDO_TRAINING_GROUND", "Gerudo Training Ground (Men)", "Men"),
    ("SCENE_THIEVES_HIDEOUT", "Thieves' Hideout (Gerudoway)", "Gerudoway"),
    ("SCENE_INSIDE_GANONS_CASTLE", "Inside Ganon's Castle (Ganontika)", "Ganontika"),
    ("SCENE_GANONS_TOWER_COLLAPSE_INTERIOR", "Ganon's Tower (Collapsing) (Ganon Sonogo)", "Ganon Sonogo"),
    (
        "SCENE_INSIDE_GANONS_CASTLE_COLLAPSE",
        "Inside Ganon's Castle (Collapsing) (Ganontika Sonogo)",
        "Ganontika Sonogo",
    ),
    ("SCENE_TREASURE_BOX_SHOP", "Treasure Chest Shop (Takaraya)", "Takaraya"),
    ("SCENE_DEKU_TREE_BOSS", "Gohma's Lair (Ydan Boss)", "Ydan Boss"),
    ("SCENE_DODONGOS_CAVERN_BOSS", "King Dodongo's Lair (Ddan Boss)", "Ddan Boss"),
    ("SCENE_JABU_JABU_BOSS", "Barinade's Lair (Bdan Boss)", "Bdan Boss"),
    ("SCENE_FOREST_TEMPLE_BOSS", "Phantom Ganon's Lair (Moribossroom)", "Moribossroom"),
    ("SCENE_FIRE_TEMPLE_BOSS", "Volvagia's Lair (Fire Bs)", "Fire Bs"),
    ("SCENE_WATER_TEMPLE_BOSS", "Morpha's Lair (Mizusin Bs)", "Mizusin Bs"),
    ("SCENE_SPIRIT_TEMPLE_BOSS", "Twinrova's Lair & Iron Knuckle Mini-Boss Room (Jyasinboss)", "Jyasinboss"),
    ("SCENE_SHADOW_TEMPLE_BOSS", "Bongo Bongo's Lair (Hakadan Bs)", "Hakadan Bs"),
    ("SCENE_GANONDORF_BOSS", "Ganondorf's Lair (Ganon Boss)", "Ganon Boss"),
    (
        "SCENE_GANONS_TOWER_COLLAPSE_EXTERIOR",
        "Ganondorf's Death Scene (Tower Escape Exterior) (Ganon Final)",
        "Ganon Final",
    ),
    ("SCENE_MARKET_ENTRANCE_DAY", "Market Entrance (Child - Day) (Entra)", "Entra"),
    ("SCENE_MARKET_ENTRANCE_NIGHT", "Market Entrance (Child - Night) (Entra N)", "Entra N"),
    ("SCENE_MARKET_ENTRANCE_RUINS", "Market Entrance (Ruins) (Enrui)", "Enrui"),
    ("SCENE_BACK_ALLEY_DAY", "Back Alley (Day) (Market Alley)", "Market Alley"),
    ("SCENE_BACK_ALLEY_NIGHT", "Back Alley (Night) (Market Alley N)", "Market Alley N"),
    ("SCENE_MARKET_DAY", "Market (Child - Day) (Market Day)", "Market Day"),
    ("SCENE_MARKET_NIGHT", "Market (Child - Night) (Market Night)", "Market Night"),
    ("SCENE_MARKET_RUINS", "Market (Ruins) (Market Ruins)", "Market Ruins"),
    ("SCENE_TEMPLE_OF_TIME_EXTERIOR_DAY", "Temple of Time Exterior (Day) (Shrine)", "Shrine"),
    ("SCENE_TEMPLE_OF_TIME_EXTERIOR_NIGHT", "Temple of Time Exterior (Night) (Shrine N)", "Shrine N"),
    ("SCENE_TEMPLE_OF_TIME_EXTERIOR_RUINS", "Temple of Time Exterior (Ruins) (Shrine R)", "Shrine R"),
    ("SCENE_KNOW_IT_ALL_BROS_HOUSE", "Know-It-All Brothers' House (Kokiri Home)", "Kokiri Home"),
    ("SCENE_TWINS_HOUSE", "Twins' House (Kokiri Home3)", "Kokiri Home3"),
    ("SCENE_MIDOS_HOUSE", "Mido's House (Kokiri Home4)", "Kokiri Home4"),
    ("SCENE_SARIAS_HOUSE", "Saria's House (Kokiri Home5)", "Kokiri Home5"),
    ("SCENE_KAKARIKO_CENTER_GUEST_HOUSE", "Carpenter Boss's House (Kakariko)", "Kakariko"),
    ("SCENE_BACK_ALLEY_HOUSE", "Back Alley House (Man in Green) (Kakariko3)", "Kakariko3"),
    ("SCENE_BAZAAR", "Bazaar (Shop1)", "Shop1"),
    ("SCENE_KOKIRI_SHOP", "Kokiri Shop (Kokiri Shop)", "Kokiri Shop"),
    ("SCENE_GORON_SHOP", "Goron Shop (Golon)", "Golon"),
    ("SCENE_ZORA_SHOP", "Zora Shop (Zoora)", "Zoora"),
    ("SCENE_POTION_SHOP_KAKARIKO", "Kakariko Potion Shop (Drag)", "Drag"),
    ("SCENE_POTION_SHOP_MARKET", "Market Potion Shop (Alley Shop)", "Alley Shop"),
    ("SCENE_BOMBCHU_SHOP", "Bombchu Shop (Night Shop)", "Night Shop"),
    ("SCENE_HAPPY_MASK_SHOP", "Happy Mask Shop (Face Shop)", "Face Shop"),
    ("SCENE_LINKS_HOUSE", "Link's House (Link Home)", "Link Home"),
    ("SCENE_DOG_LADY_HOUSE", "Back Alley House (Dog Lady) (Impa)", "Impa"),
    ("SCENE_STABLE", "Stable (Malon Stable)", "Malon Stable"),
    ("SCENE_IMPAS_HOUSE", "Impa's House (Labo)", "Labo"),
    ("SCENE_LAKESIDE_LABORATORY", "Lakeside Laboratory (Hylia Labo)", "Hylia Labo"),
    ("SCENE_CARPENTERS_TENT", "Carpenters' Tent (Tent)", "Tent"),
    ("SCENE_GRAVEKEEPERS_HUT", "Gravekeeper's Hut (Hut)", "Hut"),
    ("SCENE_GREAT_FAIRYS_FOUNTAIN_MAGIC", "Great Fairy's Fountain (Upgrades) (Daiyousei Izumi)", "Daiyousei Izumi"),
    ("SCENE_FAIRYS_FOUNTAIN", "Fairy's Fountain (Healing Fairies) (Yousei Izumi Tate)", "Yousei Izumi Tate"),
    ("SCENE_GREAT_FAIRYS_FOUNTAIN_SPELLS", "Great Fairy's Fountain (Spells) (Yousei Izumi Yoko)", "Yousei Izumi Yoko"),
    ("SCENE_GROTTOS", "Grottos (Kakusiana)", "Kakusiana"),
    ("SCENE_REDEAD_GRAVE", "Grave (Redead) (Hakaana)", "Hakaana"),
    ("SCENE_GRAVE_WITH_FAIRYS_FOUNTAIN", "Grave (Fairy's Fountain) (Hakaana2)", "Hakaana2"),
    ("SCENE_ROYAL_FAMILYS_TOMB", "Royal Family's Tomb (Hakaana Ouke)", "Hakaana Ouke"),
    ("SCENE_SHOOTING_GALLERY", "Shooting Gallery (Syatekijyou)", "Syatekijyou"),
    ("SCENE_TEMPLE_OF_TIME", "Temple of Time (Tokinoma)", "Tokinoma"),
    ("SCENE_CHAMBER_OF_THE_SAGES", "Chamber of the Sages (Kenjyanoma)", "Kenjyanoma"),
    ("SCENE_CASTLE_COURTYARD_GUARDS_DAY", "Castle Hedge Maze (Day) (Hairal Niwa)", "Hairal Niwa"),
    ("SCENE_CASTLE_COURTYARD_GUARDS_NIGHT", "Castle Hedge Maze (Night) (Hairal Niwa N)", "Hairal Niwa N"),
    ("SCENE_CUTSCENE_MAP", "Cutscene Map (Hiral Demo)", "Hiral Demo"),
    ("SCENE_WINDMILL_AND_DAMPES_GRAVE", "Dampé's Grave & Windmill (Hakasitarelay)", "Hakasitarelay"),
    ("SCENE_FISHING_POND", "Fishing Pond (Turibori)", "Turibori"),
    ("SCENE_CASTLE_COURTYARD_ZELDA", "Castle Courtyard (Nakaniwa)", "Nakaniwa"),
    ("SCENE_BOMBCHU_BOWLING_ALLEY", "Bombchu Bowling Alley (Bowling)", "Bowling"),
    ("SCENE_LON_LON_BUILDINGS", "Lon Lon Ranch House & Tower (Souko)", "Souko"),
    ("SCENE_MARKET_GUARD_HOUSE", "Guard House (Miharigoya)", "Miharigoya"),
    ("SCENE_POTION_SHOP_GRANNY", "Granny's Potion Shop (Mahouya)", "Mahouya"),
    ("SCENE_GANON_BOSS", "Ganon's Tower Collapse & Battle Arena (Ganon Demo)", "Ganon Demo"),
    ("SCENE_HOUSE_OF_SKULLTULA", "House of Skulltula (Kinsuta)", "Kinsuta"),
    ("SCENE_HYRULE_FIELD", "Hyrule Field (Spot00)", "Spot00"),
    ("SCENE_KAKARIKO_VILLAGE", "Kakariko Village (Spot01)", "Spot01"),
    ("SCENE_GRAVEYARD", "Graveyard (Spot02)", "Spot02"),
    ("SCENE_ZORAS_RIVER", "Zora's River (Spot03)", "Spot03"),
    ("SCENE_KOKIRI_FOREST", "Kokiri Forest (Spot04)", "Spot04"),
    ("SCENE_SACRED_FOREST_MEADOW", "Sacred Forest Meadow (Spot05)", "Spot05"),
    ("SCENE_LAKE_HYLIA", "Lake Hylia (Spot06)", "Spot06"),
    ("SCENE_ZORAS_DOMAIN", "Zora's Domain (Spot07)", "Spot07"),
    ("SCENE_ZORAS_FOUNTAIN", "Zora's Fountain (Spot08)", "Spot08"),
    ("SCENE_GERUDO_VALLEY", "Gerudo Valley (Spot09)", "Spot09"),
    ("SCENE_LOST_WOODS", "Lost Woods (Spot10)", "Spot10"),
    ("SCENE_DESERT_COLOSSUS", "Desert Colossus (Spot11)", "Spot11"),
    ("SCENE_GERUDOS_FORTRESS", "Gerudo's Fortress (Spot12)", "Spot12"),
    ("SCENE_HAUNTED_WASTELAND", "Haunted Wasteland (Spot13)", "Spot13"),
    ("SCENE_HYRULE_CASTLE", "Hyrule Castle (Spot15)", "Spot15"),
    ("SCENE_DEATH_MOUNTAIN_TRAIL", "Death Mountain Trail (Spot16)", "Spot16"),
    ("SCENE_DEATH_MOUNTAIN_CRATER", "Death Mountain Crater (Spot17)", "Spot17"),
    ("SCENE_GORON_CITY", "Goron City (Spot18)", "Spot18"),
    ("SCENE_LON_LON_RANCH", "Lon Lon Ranch (Spot20)", "Spot20"),
    ("SCENE_OUTSIDE_GANONS_CASTLE", "Ganon's Castle Exterior (Ganon Tou)", "Ganon Tou"),
    ("SCENE_TEST01", "Jungle Gym (Test01)", "Test01"),
    ("SCENE_BESITU", "Ganondorf Test Room (Besitu)", "Besitu"),
    ("SCENE_DEPTH_TEST", "Depth Test (Depth Test)", "Depth Test"),
    ("SCENE_SYOTES", "Stalfos Mini-Boss Room (Syotes)", "Syotes"),
    ("SCENE_SYOTES2", "Stalfos Boss ROom (Syotes2)", "Syotes2"),
    ("SCENE_SUTARU", "Sutaru (Sutaru)", "Sutaru"),
    ("SCENE_HAIRAL_NIWA2", "Castle Hedge Maze (Early) (Hairal Niwa2)", "Hairal Niwa2"),
    ("SCENE_SASATEST", "Sasatest (Sasatest)", "Sasatest"),
    ("SCENE_TESTROOM", "Treasure Chest Room (Testroom)", "Testroom"),
]

# The order of this list matters (normal MM scene order as defined by ``scene_table.h``)
mm_enum_scene_id = [
    ("Custom", "Custom", "Custom"),
    ("SCENE_20SICHITAI2", "Southern Swamp (Clear) (Z2_20SICHITAI2)", "Z2_20SICHITAI2"),
    ("SCENE_KAKUSIANA", "Lone Peak Shrine & Grottos (KAKUSIANA)", "KAKUSIANA"),
    ("SCENE_SPOT00", "Cutscene Scene (SPOT00)", "SPOT00"),
    ("SCENE_WITCH_SHOP", "Magic Hags' Potion Shop (Z2_WITCH_SHOP)", "Z2_WITCH_SHOP"),
    ("SCENE_LAST_BS", "Majora's Lair (Z2_LAST_BS)", "Z2_LAST_BS"),
    ("SCENE_HAKASHITA", "Beneath the Graveyard (Z2_HAKASHITA)", "Z2_HAKASHITA"),
    ("SCENE_AYASHIISHOP", "Curiosity Shop (Z2_AYASHIISHOP)", "Z2_AYASHIISHOP"),
    ("SCENE_OMOYA", "Mama's House (Ranch House in PAL) & Barn (Z2_OMOYA)", "Z2_OMOYA"),
    ("SCENE_BOWLING", "Honey & Darling's Shop (Z2_BOWLING)", "Z2_BOWLING"),
    ("SCENE_SONCHONOIE", "The Mayor's Residence (Z2_SONCHONOIE)", "Z2_SONCHONOIE"),
    ("SCENE_IKANA", "Ikana Canyon (Z2_IKANA)", "Z2_IKANA"),
    ("SCENE_KAIZOKU", "Pirates' Fortress (Z2_KAIZOKU)", "Z2_KAIZOKU"),
    ("SCENE_MILK_BAR", "Milk Bar (Z2_MILK_BAR)", "Z2_MILK_BAR"),
    ("SCENE_INISIE_N", "Stone Tower Temple (Z2_INISIE_N)", "Z2_INISIE_N"),
    ("SCENE_TAKARAYA", "Treasure Chest Shop (Z2_TAKARAYA)", "Z2_TAKARAYA"),
    ("SCENE_INISIE_R", "Inverted Stone Tower Temple (Z2_INISIE_R)", "Z2_INISIE_R"),
    ("SCENE_OKUJOU", "Clock Tower Rooftop (Z2_OKUJOU)", "Z2_OKUJOU"),
    ("SCENE_OPENINGDAN", "Before Clock Town (Z2_OPENINGDAN)", "Z2_OPENINGDAN"),
    ("SCENE_MITURIN", "Woodfall Temple (Z2_MITURIN)", "Z2_MITURIN"),
    ("SCENE_13HUBUKINOMITI", "Path to Mountain Village (Z2_13HUBUKINOMITI)", "Z2_13HUBUKINOMITI"),
    ("SCENE_CASTLE", "Ancient Castle of Ikana (Z2_CASTLE)", "Z2_CASTLE"),
    ("SCENE_DEKUTES", "Deku Scrub Playground (Z2_DEKUTES)", "Z2_DEKUTES"),
    ("SCENE_MITURIN_BS", "Odolwa's Lair (Z2_MITURIN_BS)", "Z2_MITURIN_BS"),
    ("SCENE_SYATEKI_MIZU", "Town Shooting Gallery (Z2_SYATEKI_MIZU)", "Z2_SYATEKI_MIZU"),
    ("SCENE_HAKUGIN", "Snowhead Temple (Z2_HAKUGIN)", "Z2_HAKUGIN"),
    ("SCENE_ROMANYMAE", "Milk Road (Z2_ROMANYMAE)", "Z2_ROMANYMAE"),
    ("SCENE_PIRATE", "Pirates' Fortress Interior (Z2_PIRATE)", "Z2_PIRATE"),
    ("SCENE_SYATEKI_MORI", "Swamp Shooting Gallery (Z2_SYATEKI_MORI)", "Z2_SYATEKI_MORI"),
    ("SCENE_SINKAI", "Pinnacle Rock (Z2_SINKAI)", "Z2_SINKAI"),
    ("SCENE_YOUSEI_IZUMI", "Fairy's Fountain (Z2_YOUSEI_IZUMI)", "Z2_YOUSEI_IZUMI"),
    ("SCENE_KINSTA1", "Swamp Spider House (Z2_KINSTA1)", "Z2_KINSTA1"),
    ("SCENE_KINDAN2", "Oceanside Spider House (Z2_KINDAN2)", "Z2_KINDAN2"),
    ("SCENE_TENMON_DAI", "Astral Observatory (Z2_TENMON_DAI)", "Z2_TENMON_DAI"),
    ("SCENE_LAST_DEKU", "Moon Deku Trial (Z2_LAST_DEKU)", "Z2_LAST_DEKU"),
    ("SCENE_22DEKUCITY", "Deku Palace (Z2_22DEKUCITY)", "Z2_22DEKUCITY"),
    ("SCENE_KAJIYA", "Mountain Smithy (Z2_KAJIYA)", "Z2_KAJIYA"),
    ("SCENE_00KEIKOKU", "Termina Field (Z2_00KEIKOKU)", "Z2_00KEIKOKU"),
    ("SCENE_POSTHOUSE", "Post Office (Z2_POSTHOUSE)", "Z2_POSTHOUSE"),
    ("SCENE_LABO", "Marine Research Lab (Z2_LABO)", "Z2_LABO"),
    ("SCENE_DANPEI2TEST", "Beneath the Graveyard (Day 3) and Dampe's House (Z2_DANPEI2TEST)", "Z2_DANPEI2TEST"),
    ("SCENE_16GORON_HOUSE", "Goron Shrine (Z2_16GORON_HOUSE)", "Z2_16GORON_HOUSE"),
    ("SCENE_33ZORACITY", "Zora Hall (Z2_33ZORACITY)", "Z2_33ZORACITY"),
    ("SCENE_8ITEMSHOP", "Trading Post (Z2_8ITEMSHOP)", "Z2_8ITEMSHOP"),
    ("SCENE_F01", "Romani Ranch (Z2_F01)", "Z2_F01"),
    ("SCENE_INISIE_BS", "Twinmold's Lair (Z2_INISIE_BS)", "Z2_INISIE_BS"),
    ("SCENE_30GYOSON", "Great Bay Coast (Z2_30GYOSON)", "Z2_30GYOSON"),
    ("SCENE_31MISAKI", "Zora Cape (Z2_31MISAKI)", "Z2_31MISAKI"),
    ("SCENE_TAKARAKUJI", "Lottery Shop (Z2_TAKARAKUJI)", "Z2_TAKARAKUJI"),
    ("SCENE_TORIDE", "Pirates' Fortress Moat (Z2_TORIDE)", "Z2_TORIDE"),
    ("SCENE_FISHERMAN", "Fisherman's Hut (Z2_FISHERMAN)", "Z2_FISHERMAN"),
    ("SCENE_GORONSHOP", "Goron Shop (Z2_GORONSHOP)", "Z2_GORONSHOP"),
    ("SCENE_DEKU_KING", "Deku King's Chamber (Z2_DEKU_KING)", "Z2_DEKU_KING"),
    ("SCENE_LAST_GORON", "Moon Goron Trial (Z2_LAST_GORON)", "Z2_LAST_GORON"),
    ("SCENE_24KEMONOMITI", "Road to Southern Swamp (Z2_24KEMONOMITI)", "Z2_24KEMONOMITI"),
    ("SCENE_F01_B", "Doggy Racetrack (Z2_F01_B)", "Z2_F01_B"),
    ("SCENE_F01C", "Cucco Shack (Z2_F01C)", "Z2_F01C"),
    ("SCENE_BOTI", "Ikana Graveyard (Z2_BOTI)", "Z2_BOTI"),
    ("SCENE_HAKUGIN_BS", "Goht's Lair (Z2_HAKUGIN_BS)", "Z2_HAKUGIN_BS"),
    ("SCENE_20SICHITAI", "Southern Swamp (poison) (Z2_20SICHITAI)", "Z2_20SICHITAI"),
    ("SCENE_21MITURINMAE", "Woodfall (Z2_21MITURINMAE)", "Z2_21MITURINMAE"),
    ("SCENE_LAST_ZORA", "Moon Zora Trial (Z2_LAST_ZORA)", "Z2_LAST_ZORA"),
    ("SCENE_11GORONNOSATO2", "Goron Village (spring) (Z2_11GORONNOSATO2)", "Z2_11GORONNOSATO2"),
    ("SCENE_SEA", "Great Bay Temple (Z2_SEA)", "Z2_SEA"),
    ("SCENE_35TAKI", "Waterfall Rapids (Z2_35TAKI)", "Z2_35TAKI"),
    ("SCENE_REDEAD", "Beneath the Well (Z2_REDEAD)", "Z2_REDEAD"),
    ("SCENE_BANDROOM", "Zora Hall Rooms (Z2_BANDROOM)", "Z2_BANDROOM"),
    ("SCENE_11GORONNOSATO", "Goron Village (winter) (Z2_11GORONNOSATO)", "Z2_11GORONNOSATO"),
    ("SCENE_GORON_HAKA", "Goron Graveyard (Z2_GORON_HAKA)", "Z2_GORON_HAKA"),
    ("SCENE_SECOM", "Sakon's Hideout (Z2_SECOM)", "Z2_SECOM"),
    ("SCENE_10YUKIYAMANOMURA", "Mountain Village (winter) (Z2_10YUKIYAMANOMURA)", "Z2_10YUKIYAMANOMURA"),
    ("SCENE_TOUGITES", "Ghost Hut (Z2_TOUGITES)", "Z2_TOUGITES"),
    ("SCENE_DANPEI", "Deku Shrine (Z2_DANPEI)", "Z2_DANPEI"),
    ("SCENE_IKANAMAE", "Road to Ikana (Z2_IKANAMAE)", "Z2_IKANAMAE"),
    ("SCENE_DOUJOU", "Swordsman's School (Z2_DOUJOU)", "Z2_DOUJOU"),
    ("SCENE_MUSICHOUSE", "Music Box House (Z2_MUSICHOUSE)", "Z2_MUSICHOUSE"),
    ("SCENE_IKNINSIDE", "Igos du Ikana's Lair (Z2_IKNINSIDE)", "Z2_IKNINSIDE"),
    ("SCENE_MAP_SHOP", "Tourist Information (Z2_MAP_SHOP)", "Z2_MAP_SHOP"),
    ("SCENE_F40", "Stone Tower (Z2_F40)", "Z2_F40"),
    ("SCENE_F41", "Inverted Stone Tower (Z2_F41)", "Z2_F41"),
    ("SCENE_10YUKIYAMANOMURA2", "Mountain Village (spring) (Z2_10YUKIYAMANOMURA2)", "Z2_10YUKIYAMANOMURA2"),
    ("SCENE_14YUKIDAMANOMITI", "Path to Snowhead (Z2_14YUKIDAMANOMITI)", "Z2_14YUKIDAMANOMITI"),
    ("SCENE_12HAKUGINMAE", "Snowhead (Z2_12HAKUGINMAE)", "Z2_12HAKUGINMAE"),
    ("SCENE_17SETUGEN", "Path to Goron Village (winter) (Z2_17SETUGEN)", "Z2_17SETUGEN"),
    ("SCENE_17SETUGEN2", "Path to Goron Village (spring) (Z2_17SETUGEN2)", "Z2_17SETUGEN2"),
    ("SCENE_SEA_BS", "Gyorg's Lair (Z2_SEA_BS)", "Z2_SEA_BS"),
    ("SCENE_RANDOM", "Secret Shrine (Z2_RANDOM)", "Z2_RANDOM"),
    ("SCENE_YADOYA", "Stock Pot Inn (Z2_YADOYA)", "Z2_YADOYA"),
    ("SCENE_KONPEKI_ENT", "Great Bay Cutscene (Z2_KONPEKI_ENT)", "Z2_KONPEKI_ENT"),
    ("SCENE_INSIDETOWER", "Clock Tower Interior (Z2_INSIDETOWER)", "Z2_INSIDETOWER"),
    ("SCENE_26SARUNOMORI", "Woods of Mystery (Z2_26SARUNOMORI)", "Z2_26SARUNOMORI"),
    ("SCENE_LOST_WOODS", "Lost Woods (Intro) (Z2_LOST_WOODS)", "Z2_LOST_WOODS"),
    ("SCENE_LAST_LINK", "Moon Link Trial (Z2_LAST_LINK)", "Z2_LAST_LINK"),
    ("SCENE_SOUGEN", "The Moon (Z2_SOUGEN)", "Z2_SOUGEN"),
    ("SCENE_BOMYA", "Bomb Shop (Z2_BOMYA)", "Z2_BOMYA"),
    ("SCENE_KYOJINNOMA", "Giants' Chamber (Z2_KYOJINNOMA)", "Z2_KYOJINNOMA"),
    ("SCENE_KOEPONARACE", "Gorman Track (Z2_KOEPONARACE)", "Z2_KOEPONARACE"),
    ("SCENE_GORONRACE", "Goron Racetrack (Z2_GORONRACE)", "Z2_GORONRACE"),
    ("SCENE_TOWN", "East Clock Town (Z2_TOWN)", "Z2_TOWN"),
    ("SCENE_ICHIBA", "West Clock Town (Z2_ICHIBA)", "Z2_ICHIBA"),
    ("SCENE_BACKTOWN", "North Clock Town (Z2_BACKTOWN)", "Z2_BACKTOWN"),
    ("SCENE_CLOCKTOWER", "South Clock Town (Z2_CLOCKTOWER)", "Z2_CLOCKTOWER"),
    ("SCENE_ALLEY", "Laundry Pool (Z2_ALLEY)", "Z2_ALLEY"),
]

ootSceneIDToName = {
    "SCENE_DEKU_TREE": "ydan",
    "SCENE_DODONGOS_CAVERN": "ddan",
    "SCENE_JABU_JABU": "bdan",
    "SCENE_FOREST_TEMPLE": "Bmori1",
    "SCENE_FIRE_TEMPLE": "HIDAN",
    "SCENE_WATER_TEMPLE": "MIZUsin",
    "SCENE_SPIRIT_TEMPLE": "jyasinzou",
    "SCENE_SHADOW_TEMPLE": "HAKAdan",
    "SCENE_BOTTOM_OF_THE_WELL": "HAKAdanCH",
    "SCENE_ICE_CAVERN": "ice_doukutu",
    "SCENE_GANONS_TOWER": "ganon",
    "SCENE_GERUDO_TRAINING_GROUND": "men",
    "SCENE_THIEVES_HIDEOUT": "gerudoway",
    "SCENE_INSIDE_GANONS_CASTLE": "ganontika",
    "SCENE_GANONS_TOWER_COLLAPSE_INTERIOR": "ganon_sonogo",
    "SCENE_INSIDE_GANONS_CASTLE_COLLAPSE": "ganontikasonogo",
    "SCENE_TREASURE_BOX_SHOP": "takaraya",
    "SCENE_DEKU_TREE_BOSS": "ydan_boss",
    "SCENE_DODONGOS_CAVERN_BOSS": "ddan_boss",
    "SCENE_JABU_JABU_BOSS": "bdan_boss",
    "SCENE_FOREST_TEMPLE_BOSS": "moribossroom",
    "SCENE_FIRE_TEMPLE_BOSS": "FIRE_bs",
    "SCENE_WATER_TEMPLE_BOSS": "MIZUsin_bs",
    "SCENE_SPIRIT_TEMPLE_BOSS": "jyasinboss",
    "SCENE_SHADOW_TEMPLE_BOSS": "HAKAdan_bs",
    "SCENE_GANONDORF_BOSS": "ganon_boss",
    "SCENE_GANONS_TOWER_COLLAPSE_EXTERIOR": "ganon_final",
    "SCENE_MARKET_ENTRANCE_DAY": "entra",
    "SCENE_MARKET_ENTRANCE_NIGHT": "entra_n",
    "SCENE_MARKET_ENTRANCE_RUINS": "enrui",
    "SCENE_BACK_ALLEY_DAY": "market_alley",
    "SCENE_BACK_ALLEY_NIGHT": "market_alley_n",
    "SCENE_MARKET_DAY": "market_day",
    "SCENE_MARKET_NIGHT": "market_night",
    "SCENE_MARKET_RUINS": "market_ruins",
    "SCENE_TEMPLE_OF_TIME_EXTERIOR_DAY": "shrine",
    "SCENE_TEMPLE_OF_TIME_EXTERIOR_NIGHT": "shrine_n",
    "SCENE_TEMPLE_OF_TIME_EXTERIOR_RUINS": "shrine_r",
    "SCENE_KNOW_IT_ALL_BROS_HOUSE": "kokiri_home",
    "SCENE_TWINS_HOUSE": "kokiri_home3",
    "SCENE_MIDOS_HOUSE": "kokiri_home4",
    "SCENE_SARIAS_HOUSE": "kokiri_home5",
    "SCENE_KAKARIKO_CENTER_GUEST_HOUSE": "kakariko",
    "SCENE_BACK_ALLEY_HOUSE": "kakariko3",
    "SCENE_BAZAAR": "shop1",
    "SCENE_KOKIRI_SHOP": "kokiri_shop",
    "SCENE_GORON_SHOP": "golon",
    "SCENE_ZORA_SHOP": "zoora",
    "SCENE_POTION_SHOP_KAKARIKO": "drag",
    "SCENE_POTION_SHOP_MARKET": "alley_shop",
    "SCENE_BOMBCHU_SHOP": "night_shop",
    "SCENE_HAPPY_MASK_SHOP": "face_shop",
    "SCENE_LINKS_HOUSE": "link_home",
    "SCENE_DOG_LADY_HOUSE": "impa",
    "SCENE_STABLE": "malon_stable",
    "SCENE_IMPAS_HOUSE": "labo",
    "SCENE_LAKESIDE_LABORATORY": "hylia_labo",
    "SCENE_CARPENTERS_TENT": "tent",
    "SCENE_GRAVEKEEPERS_HUT": "hut",
    "SCENE_GREAT_FAIRYS_FOUNTAIN_MAGIC": "daiyousei_izumi",
    "SCENE_FAIRYS_FOUNTAIN": "yousei_izumi_tate",
    "SCENE_GREAT_FAIRYS_FOUNTAIN_SPELLS": "yousei_izumi_yoko",
    "SCENE_GROTTOS": "kakusiana",
    "SCENE_REDEAD_GRAVE": "hakaana",
    "SCENE_GRAVE_WITH_FAIRYS_FOUNTAIN": "hakaana2",
    "SCENE_ROYAL_FAMILYS_TOMB": "hakaana_ouke",
    "SCENE_SHOOTING_GALLERY": "syatekijyou",
    "SCENE_TEMPLE_OF_TIME": "tokinoma",
    "SCENE_CHAMBER_OF_THE_SAGES": "kenjyanoma",
    "SCENE_CASTLE_COURTYARD_GUARDS_DAY": "hairal_niwa",
    "SCENE_CASTLE_COURTYARD_GUARDS_NIGHT": "hairal_niwa_n",
    "SCENE_CUTSCENE_MAP": "hiral_demo",
    "SCENE_WINDMILL_AND_DAMPES_GRAVE": "hakasitarelay",
    "SCENE_FISHING_POND": "turibori",
    "SCENE_CASTLE_COURTYARD_ZELDA": "nakaniwa",
    "SCENE_BOMBCHU_BOWLING_ALLEY": "bowling",
    "SCENE_LON_LON_BUILDINGS": "souko",
    "SCENE_MARKET_GUARD_HOUSE": "miharigoya",
    "SCENE_POTION_SHOP_GRANNY": "mahouya",
    "SCENE_GANON_BOSS": "ganon_demo",
    "SCENE_HOUSE_OF_SKULLTULA": "kinsuta",
    "SCENE_HYRULE_FIELD": "spot00",
    "SCENE_KAKARIKO_VILLAGE": "spot01",
    "SCENE_GRAVEYARD": "spot02",
    "SCENE_ZORAS_RIVER": "spot03",
    "SCENE_KOKIRI_FOREST": "spot04",
    "SCENE_SACRED_FOREST_MEADOW": "spot05",
    "SCENE_LAKE_HYLIA": "spot06",
    "SCENE_ZORAS_DOMAIN": "spot07",
    "SCENE_ZORAS_FOUNTAIN": "spot08",
    "SCENE_GERUDO_VALLEY": "spot09",
    "SCENE_LOST_WOODS": "spot10",
    "SCENE_DESERT_COLOSSUS": "spot11",
    "SCENE_GERUDOS_FORTRESS": "spot12",
    "SCENE_HAUNTED_WASTELAND": "spot13",
    "SCENE_HYRULE_CASTLE": "spot15",
    "SCENE_DEATH_MOUNTAIN_TRAIL": "spot16",
    "SCENE_DEATH_MOUNTAIN_CRATER": "spot17",
    "SCENE_GORON_CITY": "spot18",
    "SCENE_LON_LON_RANCH": "spot20",
    "SCENE_OUTSIDE_GANONS_CASTLE": "ganon_tou",
    "SCENE_TEST01": "test01",
    "SCENE_BESITU": "besitu",
    "SCENE_DEPTH_TEST": "depth_test",
    "SCENE_SYOTES": "syotes",
    "SCENE_SYOTES2": "syotes2",
    "SCENE_SUTARU": "sutaru",
    "SCENE_HAIRAL_NIWA2": "hairal_niwa2",
    "SCENE_SASATEST": "sasatest",
    "SCENE_TESTROOM": "testroom",
}
ootSceneNameToID = {val: key for key, val in ootSceneIDToName.items()}

mm_scene_id_to_name = {
    "SCENE_20SICHITAI2": "Z2_20SICHITAI2",
    "SCENE_KAKUSIANA": "KAKUSIANA",
    "SCENE_SPOT00": "SPOT00",
    "SCENE_WITCH_SHOP": "Z2_WITCH_SHOP",
    "SCENE_LAST_BS": "Z2_LAST_BS",
    "SCENE_HAKASHITA": "Z2_HAKASHITA",
    "SCENE_AYASHIISHOP": "Z2_AYASHIISHOP",
    "SCENE_OMOYA": "Z2_OMOYA",
    "SCENE_BOWLING": "Z2_BOWLING",
    "SCENE_SONCHONOIE": "Z2_SONCHONOIE",
    "SCENE_IKANA": "Z2_IKANA",
    "SCENE_KAIZOKU": "Z2_KAIZOKU",
    "SCENE_MILK_BAR": "Z2_MILK_BAR",
    "SCENE_INISIE_N": "Z2_INISIE_N",
    "SCENE_TAKARAYA": "Z2_TAKARAYA",
    "SCENE_INISIE_R": "Z2_INISIE_R",
    "SCENE_OKUJOU": "Z2_OKUJOU",
    "SCENE_OPENINGDAN": "Z2_OPENINGDAN",
    "SCENE_MITURIN": "Z2_MITURIN",
    "SCENE_13HUBUKINOMITI": "Z2_13HUBUKINOMITI",
    "SCENE_CASTLE": "Z2_CASTLE",
    "SCENE_DEKUTES": "Z2_DEKUTES",
    "SCENE_MITURIN_BS": "Z2_MITURIN_BS",
    "SCENE_SYATEKI_MIZU": "Z2_SYATEKI_MIZU",
    "SCENE_HAKUGIN": "Z2_HAKUGIN",
    "SCENE_ROMANYMAE": "Z2_ROMANYMAE",
    "SCENE_PIRATE": "Z2_PIRATE",
    "SCENE_SYATEKI_MORI": "Z2_SYATEKI_MORI",
    "SCENE_SINKAI": "Z2_SINKAI",
    "SCENE_YOUSEI_IZUMI": "Z2_YOUSEI_IZUMI",
    "SCENE_KINSTA1": "Z2_KINSTA1",
    "SCENE_KINDAN2": "Z2_KINDAN2",
    "SCENE_TENMON_DAI": "Z2_TENMON_DAI",
    "SCENE_LAST_DEKU": "Z2_LAST_DEKU",
    "SCENE_22DEKUCITY": "Z2_22DEKUCITY",
    "SCENE_KAJIYA": "Z2_KAJIYA",
    "SCENE_00KEIKOKU": "Z2_00KEIKOKU",
    "SCENE_POSTHOUSE": "Z2_POSTHOUSE",
    "SCENE_LABO": "Z2_LABO",
    "SCENE_DANPEI2TEST": "Z2_DANPEI2TEST",
    "SCENE_16GORON_HOUSE": "Z2_16GORON_HOUSE",
    "SCENE_33ZORACITY": "Z2_33ZORACITY",
    "SCENE_8ITEMSHOP": "Z2_8ITEMSHOP",
    "SCENE_F01": "Z2_F01",
    "SCENE_INISIE_BS": "Z2_INISIE_BS",
    "SCENE_30GYOSON": "Z2_30GYOSON",
    "SCENE_31MISAKI": "Z2_31MISAKI",
    "SCENE_TAKARAKUJI": "Z2_TAKARAKUJI",
    "SCENE_TORIDE": "Z2_TORIDE",
    "SCENE_FISHERMAN": "Z2_FISHERMAN",
    "SCENE_GORONSHOP": "Z2_GORONSHOP",
    "SCENE_DEKU_KING": "Z2_DEKU_KING",
    "SCENE_LAST_GORON": "Z2_LAST_GORON",
    "SCENE_24KEMONOMITI": "Z2_24KEMONOMITI",
    "SCENE_F01_B": "Z2_F01_B",
    "SCENE_F01C": "Z2_F01C",
    "SCENE_BOTI": "Z2_BOTI",
    "SCENE_HAKUGIN_BS": "Z2_HAKUGIN_BS",
    "SCENE_20SICHITAI": "Z2_20SICHITAI",
    "SCENE_21MITURINMAE": "Z2_21MITURINMAE",
    "SCENE_LAST_ZORA": "Z2_LAST_ZORA",
    "SCENE_11GORONNOSATO2": "Z2_11GORONNOSATO2",
    "SCENE_SEA": "Z2_SEA",
    "SCENE_35TAKI": "Z2_35TAKI",
    "SCENE_REDEAD": "Z2_REDEAD",
    "SCENE_BANDROOM": "Z2_BANDROOM",
    "SCENE_11GORONNOSATO": "Z2_11GORONNOSATO",
    "SCENE_GORON_HAKA": "Z2_GORON_HAKA",
    "SCENE_SECOM": "Z2_SECOM",
    "SCENE_10YUKIYAMANOMURA": "Z2_10YUKIYAMANOMURA",
    "SCENE_TOUGITES": "Z2_TOUGITES",
    "SCENE_DANPEI": "Z2_DANPEI",
    "SCENE_IKANAMAE": "Z2_IKANAMAE",
    "SCENE_DOUJOU": "Z2_DOUJOU",
    "SCENE_MUSICHOUSE": "Z2_MUSICHOUSE",
    "SCENE_IKNINSIDE": "Z2_IKNINSIDE",
    "SCENE_MAP_SHOP": "Z2_MAP_SHOP",
    "SCENE_F40": "Z2_F40",
    "SCENE_F41": "Z2_F41",
    "SCENE_10YUKIYAMANOMURA2": "Z2_10YUKIYAMANOMURA2",
    "SCENE_14YUKIDAMANOMITI": "Z2_14YUKIDAMANOMITI",
    "SCENE_12HAKUGINMAE": "Z2_12HAKUGINMAE",
    "SCENE_17SETUGEN": "Z2_17SETUGEN",
    "SCENE_17SETUGEN2": "Z2_17SETUGEN2",
    "SCENE_SEA_BS": "Z2_SEA_BS",
    "SCENE_RANDOM": "Z2_RANDOM",
    "SCENE_YADOYA": "Z2_YADOYA",
    "SCENE_KONPEKI_ENT": "Z2_KONPEKI_ENT",
    "SCENE_INSIDETOWER": "Z2_INSIDETOWER",
    "SCENE_26SARUNOMORI": "Z2_26SARUNOMORI",
    "SCENE_LOST_WOODS": "Z2_LOST_WOODS",
    "SCENE_LAST_LINK": "Z2_LAST_LINK",
    "SCENE_SOUGEN": "Z2_SOUGEN",
    "SCENE_BOMYA": "Z2_BOMYA",
    "SCENE_KYOJINNOMA": "Z2_KYOJINNOMA",
    "SCENE_KOEPONARACE": "Z2_KOEPONARACE",
    "SCENE_GORONRACE": "Z2_GORONRACE",
    "SCENE_TOWN": "Z2_TOWN",
    "SCENE_ICHIBA": "Z2_ICHIBA",
    "SCENE_BACKTOWN": "Z2_BACKTOWN",
    "SCENE_CLOCKTOWER": "Z2_CLOCKTOWER",
    "SCENE_ALLEY": "Z2_ALLEY",
}
mm_scene_name_to_id = {val: key for key, val in mm_scene_id_to_name.items()}

ootEnumCamTransition = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "0x00", "0x00"),
    # ("0x0F", "0x0F", "0x0F"),
    # ("0xFF", "0xFF", "0xFF"),
]

# see RoomType enum
ootEnumRoomBehaviour = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "Default", "Default"),
    ("0x01", "Dungeon Behavior (Z-Target, Sun's Song)", "Dungeon Behavior (Z-Target, Sun's Song)"),
    ("0x02", "Disable Backflips/Sidehops", "Disable Backflips/Sidehops"),
    ("0x03", "Disable Color Dither", "Disable Color Dither"),
    ("0x04", "(?) Horse Camera Related", "(?) Horse Camera Related"),
    ("0x05", "Disable Darker Screen Effect (NL/Spins)", "Disable Darker Screen Effect (NL/Spins)"),
]

mm_enum_room_type = [
    ("Custom", "Custom", "Custom"),
    ("ROOM_TYPE_NORMAL", "Normal", "0x00"),
    ("ROOM_TYPE_DUNGEON", "Dungeon", "0x01"),
    ("ROOM_TYPE_INDOORS", "Indoors", "0x02"),
    ("ROOM_TYPE_3", "Type 3", "0x03"),
    ("ROOM_TYPE_4", "Type 4 (Horse related)", "0x04"),
    ("ROOM_TYPE_BOSS", "Boss", "0x05"),
]

ootEnumDrawConfig = [
    ("Custom", "Custom", "Custom"),
    ("SDC_DEFAULT", "Default", "Default"),
    ("SDC_HYRULE_FIELD", "Hyrule Field (Spot00)", "Spot00"),
    ("SDC_KAKARIKO_VILLAGE", "Kakariko Village (Spot01)", "Spot01"),
    ("SDC_ZORAS_RIVER", "Zora's River (Spot03)", "Spot03"),
    ("SDC_KOKIRI_FOREST", "Kokiri Forest (Spot04)", "Spot04"),
    ("SDC_LAKE_HYLIA", "Lake Hylia (Spot06)", "Spot06"),
    ("SDC_ZORAS_DOMAIN", "Zora's Domain (Spot07)", "Spot07"),
    ("SDC_ZORAS_FOUNTAIN", "Zora's Fountain (Spot08)", "Spot08"),
    ("SDC_GERUDO_VALLEY", "Gerudo Valley (Spot09)", "Spot09"),
    ("SDC_LOST_WOODS", "Lost Woods (Spot10)", "Spot10"),
    ("SDC_DESERT_COLOSSUS", "Desert Colossus (Spot11)", "Spot11"),
    ("SDC_GERUDOS_FORTRESS", "Gerudo's Fortress (Spot12)", "Spot12"),
    ("SDC_HAUNTED_WASTELAND", "Haunted Wasteland (Spot13)", "Spot13"),
    ("SDC_HYRULE_CASTLE", "Hyrule Castle (Spot15)", "Spot15"),
    ("SDC_DEATH_MOUNTAIN_TRAIL", "Death Mountain Trail (Spot16)", "Spot16"),
    ("SDC_DEATH_MOUNTAIN_CRATER", "Death Mountain Crater (Spot17)", "Spot17"),
    ("SDC_GORON_CITY", "Goron City (Spot18)", "Spot18"),
    ("SDC_LON_LON_RANCH", "Lon Lon Ranch (Spot20)", "Spot20"),
    ("SDC_FIRE_TEMPLE", "Fire Temple (Hidan)", "Hidan"),
    ("SDC_DEKU_TREE", "Inside the Deku Tree (Ydan)", "Ydan"),
    ("SDC_DODONGOS_CAVERN", "Dodongo's Cavern (Ddan)", "Ddan"),
    ("SDC_JABU_JABU", "Inside Jabu Jabu's Belly (Bdan)", "Bdan"),
    ("SDC_FOREST_TEMPLE", "Forest Temple (Bmori1)", "Bmori1"),
    ("SDC_WATER_TEMPLE", "Water Temple (Mizusin)", "Mizusin"),
    ("SDC_SHADOW_TEMPLE_AND_WELL", "Shadow Temple (Hakadan)", "Hakadan"),
    ("SDC_SPIRIT_TEMPLE", "Spirit Temple (Jyasinzou)", "Jyasinzou"),
    ("SDC_INSIDE_GANONS_CASTLE", "Inside Ganon's Castle (Ganontika)", "Ganontika"),
    ("SDC_GERUDO_TRAINING_GROUND", "Gerudo Training Ground (Men)", "Men"),
    ("SDC_DEKU_TREE_BOSS", "Gohma's Lair (Ydan Boss)", "Ydan Boss"),
    ("SDC_WATER_TEMPLE_BOSS", "Morpha's Lair (Mizusin Bs)", "Mizusin Bs"),
    ("SDC_TEMPLE_OF_TIME", "Temple of Time (Tokinoma)", "Tokinoma"),
    ("SDC_GROTTOS", "Grottos (Kakusiana)", "Kakusiana"),
    ("SDC_CHAMBER_OF_THE_SAGES", "Chamber of the Sages (Kenjyanoma)", "Kenjyanoma"),
    ("SDC_GREAT_FAIRYS_FOUNTAIN", "Great Fairy Fountain", "Great Fairy Fountain"),
    ("SDC_SHOOTING_GALLERY", "Shooting Gallery (Syatekijyou)", "Syatekijyou"),
    ("SDC_CASTLE_COURTYARD_GUARDS", "Castle Hedge Maze (Day) (Hairal Niwa)", "Hairal Niwa"),
    ("SDC_OUTSIDE_GANONS_CASTLE", "Ganon's Castle Exterior (Ganon Tou)", "Ganon Tou"),
    ("SDC_ICE_CAVERN", "Ice Cavern (Ice Doukuto)", "Ice Doukuto"),
    (
        "SDC_GANONS_TOWER_COLLAPSE_EXTERIOR",
        "Ganondorf's Death Scene (Tower Escape Exterior) (Ganon Final)",
        "Ganon Final",
    ),
    ("SDC_FAIRYS_FOUNTAIN", "Fairy Fountain", "Fairy Fountain"),
    ("SDC_THIEVES_HIDEOUT", "Thieves' Hideout (Gerudoway)", "Gerudoway"),
    ("SDC_BOMBCHU_BOWLING_ALLEY", "Bombchu Bowling Alley (Bowling)", "Bowling"),
    ("SDC_ROYAL_FAMILYS_TOMB", "Royal Family's Tomb (Hakaana Ouke)", "Hakaana Ouke"),
    ("SDC_LAKESIDE_LABORATORY", "Lakeside Laboratory (Hylia Labo)", "Hylia Labo"),
    ("SDC_LON_LON_BUILDINGS", "Lon Lon Ranch House & Tower (Souko)", "Souko"),
    ("SDC_MARKET_GUARD_HOUSE", "Guard House (Miharigoya)", "Miharigoya"),
    ("SDC_POTION_SHOP_GRANNY", "Granny's Potion Shop (Mahouya)", "Mahouya"),
    ("SDC_CALM_WATER", "Calm Water", "Calm Water"),
    ("SDC_GRAVE_EXIT_LIGHT_SHINING", "Grave Exit Light Shining", "Grave Exit Light Shining"),
    ("SDC_BESITU", "Ganondorf Test Room (Besitu)", "Besitu"),
    ("SDC_FISHING_POND", "Fishing Pond (Turibori)", "Turibori"),
    ("SDC_GANONS_TOWER_COLLAPSE_INTERIOR", "Ganon's Tower (Collapsing) (Ganon Sonogo)", "Ganon Sonogo"),
    ("SDC_INSIDE_GANONS_CASTLE_COLLAPSE", "Inside Ganon's Castle (Collapsing) (Ganontika Sonogo)", "Ganontika Sonogo"),
]

mm_enum_draw_config = [
    ("Custom", "Custom", "Custom"),
    ("SCENE_DRAW_CFG_DEFAULT", "Default", "Default"),
    ("SCENE_DRAW_CFG_MAT_ANIM", "Material Animated", "Material Animated"),
    ("SCENE_DRAW_CFG_NOTHING", "Nothing", "Nothing"),
    ("SCENE_DRAW_CFG_GREAT_BAY_TEMPLE", "Great Bay Temple", "Great Bay Temple"),
    ("SCENE_DRAW_CFG_MAT_ANIM_MANUAL_STEP", "Material Animated (manual step)", "Material Animated (manual step)"),
]

oot_world_defaults = {
    "geometryMode": {
        "zBuffer": True,
        "shade": True,
        "cullBack": True,
        "lighting": True,
        "shadeSmooth": True,
    },
    "otherModeH": {
        "alphaDither": "G_AD_NOISE",
        "textureFilter": "G_TF_BILERP",
        "perspectiveCorrection": "G_TP_PERSP",
        "textureConvert": "G_TC_FILT",
        "cycleType": "G_CYC_2CYCLE",
    },
}
