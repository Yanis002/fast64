ootEnumConveyer = [
    ("None", "None", "None"),
    ("Land", "Land", "Land"),
    ("Water", "Water", "Water"),
]

ootEnumFloorSetting = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "Default", "Default"),
    ("0x05", "Trigger Respawn", "Trigger Respawn"),
    ("0x06", "Grab Wall", "Grab Wall"),
    ("0x08", "Stop Air Momentum", "Stop Air Momentum"),
    ("0x09", "Fall Instead Of Jumping", "Fall Instead Of Jumping"),
    ("0x0B", "Dive Animation", "Dive Animation"),
    ("0x0C", "Trigger Void", "Trigger Void"),
]

mm_enum_floor_property = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "Default", "FLOOR_PROPERTY_0"),
    ("0x01", "Frontflip Jump Animation", "FLOOR_PROPERTY_1"),
    ("0x02", "Sideflip Jump Animation", "FLOOR_PROPERTY_2"),
    ("0x05", "Trigger Respawn (sets human no mask)", "FLOOR_PROPERTY_5"),
    ("0x06", "Grab Wall", "FLOOR_PROPERTY_6"),
    ("0x07", "Unknown (sets speed to 0)", "FLOOR_PROPERTY_7"),
    ("0x08", "Stop Air Momentum", "FLOOR_PROPERTY_8"),
    ("0x09", "Fall Instead Of Jumping", "FLOOR_PROPERTY_9"),
    ("0x0B", "Dive Animation", "FLOOR_PROPERTY_11"),
    ("0x0C", "Trigger Void", "FLOOR_PROPERTY_12"),
    ("0x0D", "Trigger Void (runs `Player_Action_1`)", "FLOOR_PROPERTY_13"),
]

ootEnumWallSetting = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "Default", "Default"),
    ("0x01", "No Ledge Climb", "No Ledge Climb"),
    ("0x02", "Ladder Bottom", "Ladder Bottom"),
    ("0x03", "Ladder Top", "Ladder Top"),
    ("0x04", "Vines", "Vines"),
    ("0x05", "Crawl Space 1", "Crawl Space 1"),
    ("0x06", "Crawl Space 2", "Crawl Space 2"),
    ("0x07", "Push Block", "Push Block"),
]

ootEnumFloorProperty = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "Default", "Default"),
    ("0x01", "Haunted Wasteland Camera", "Haunted Wasteland Camera"),
    ("0x02", "Fire (damages every 6s)", "Fire (damages every 6s)"),
    ("0x03", "Fire (damages every 3s)", "Fire (damages every 3s)"),
    ("0x04", "Shallow Sand", "Shallow Sand"),
    ("0x05", "Slippery", "Slippery"),
    ("0x06", "Ignore Fall Damage", "Ignore Fall Damage"),
    ("0x07", "Quicksand Crossing (Blocks Epona)", "Quicksand Crossing (Epona Uncrossable)"),
    ("0x08", "Jabu Jabu's Belly Floor", "Jabu Jabu's Belly Floor"),
    ("0x09", "Trigger Void", "Trigger Void"),
    ("0x0A", "Stops Air Momentum", "Stops Air Momentum"),
    ("0x0B", "Grotto Exit Animation", "Link Looks Up"),
    ("0x0C", "Quicksand Crossing (Epona Crossable)", "Quicksand Crossing (Epona Crossable)"),
]

mm_enum_floor_type = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "Default", "FLOOR_TYPE_0"),
    ("0x01", "Unused (?)", "FLOOR_TYPE_1"),
    ("0x02", "Fire Damages (burns Player every second)", "FLOOR_TYPE_2"),
    ("0x03", "Fire Damages 2 (burns Player every second)", "FLOOR_TYPE_3"),
    ("0x04", "Shallow Sand", "FLOOR_TYPE_4"),
    ("0x05", "Ice (Slippery)", "FLOOR_TYPE_5"),
    ("0x06", "Ignore Fall Damages", "FLOOR_TYPE_6"),
    ("0x07", "Quicksand (blocks Epona)", "FLOOR_TYPE_7"),
    ("0x08", "Jabu Jabu's Belly Floor (Unused)", "FLOOR_TYPE_8"),
    ("0x09", "Triggers Void", "FLOOR_TYPE_9"),
    ("0x0A", "Stops Air Momentum", "FLOOR_TYPE_10"),
    ("0x0B", "Grotto Exit Animation", "FLOOR_TYPE_11"),
    ("0x0C", "Quicksand (doesn't block Epona)", "FLOOR_TYPE_12"),
    ("0x0D", "Deeper Shallow Sand", "FLOOR_TYPE_13"),
    ("0x0E", "Shallow Snow", "FLOOR_TYPE_14"),
    ("0x0F", "Deeper Shallow Snow", "FLOOR_TYPE_15"),
]

ootEnumCollisionTerrain = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "Walkable", "FLOOR_EFFECT_0"),
    ("0x01", "Steep", "FLOOR_EFFECT_1"),
    ("0x02", "Walkable (Preserves Exit Flags)", "FLOOR_EFFECT_2"),
]

mm_enum_floor_effect = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "Default", "FLOOR_EFFECT_0"),
    ("0x01", "Steep/Slippery Slope", "FLOOR_EFFECT_1"),
    ("0x02", "Walkable (Preserves Exit Flags)", "FLOOR_EFFECT_2"),
]

ootEnumCollisionSound = [
    ("Custom", "Custom", "Custom"),
    ("SURFACE_MATERIAL_DIRT", "Dirt", "Dirt (aka Earth)"),
    ("SURFACE_MATERIAL_SAND", "Sand", "Sand"),
    ("SURFACE_MATERIAL_STONE", "Stone", "Stone"),
    ("SURFACE_MATERIAL_JABU", "Jabu", "Jabu-Jabu flesh (aka Wet Stone)"),
    ("SURFACE_MATERIAL_WATER_SHALLOW", "Shallow Water", "Shallow Water"),
    ("SURFACE_MATERIAL_WATER_DEEP", "Deep Water", "Deep Water"),
    ("SURFACE_MATERIAL_TALL_GRASS", "Tall Grass", "Tall Grass"),
    ("SURFACE_MATERIAL_LAVA", "Lava", "Lava (aka Goo)"),
    ("SURFACE_MATERIAL_GRASS", "Grass", "Grass (aka Earth 2)"),
    ("SURFACE_MATERIAL_BRIDGE", "Bridge", "Bridge (aka Wooden Plank)"),
    ("SURFACE_MATERIAL_WOOD", "Wood", "Wood (aka Packed Earth)"),
    ("SURFACE_MATERIAL_DIRT_SOFT", "Soft Dirt", "Soft Dirt (aka Earth 3)"),
    ("SURFACE_MATERIAL_ICE", "Ice", "Ice (aka Ceramic)"),
    ("SURFACE_MATERIAL_CARPET", "Carpet", "Carpet (aka Loose Earth)"),
]

mm_enum_surface_material = [
    ("Custom", "Custom", "Custom"),
    ("SURFACE_MATERIAL_DIRT", "Dirt", "Dirt (aka Earth)"),
    ("SURFACE_MATERIAL_SAND", "Sand", "Sand"),
    ("SURFACE_MATERIAL_STONE", "Stone", "Stone"),
    ("SURFACE_MATERIAL_DIRT_SHALLOW", "Shallow Dirt", "Shallow Dirt"),
    ("SURFACE_MATERIAL_WATER_SHALLOW", "Shallow Water", "Shallow Water"),
    ("SURFACE_MATERIAL_WATER_DEEP", "Deep Water", "Deep Water"),
    ("SURFACE_MATERIAL_TALL_GRASS", "Tall Grass", "Tall Grass"),
    ("SURFACE_MATERIAL_LAVA", "Lava", "Lava (aka Goo)"),
    ("SURFACE_MATERIAL_GRASS", "Grass", "Grass (aka Earth 2)"),
    ("SURFACE_MATERIAL_BRIDGE", "Bridge", "Bridge (aka Wooden Plank)"),
    ("SURFACE_MATERIAL_WOOD", "Wood", "Wood (aka Packed Earth)"),
    ("SURFACE_MATERIAL_DIRT_SOFT", "Soft Dirt", "Soft Dirt (aka Earth 3)"),
    ("SURFACE_MATERIAL_ICE", "Ice", "Ice (aka Ceramic)"),
    ("SURFACE_MATERIAL_CARPET", "Carpet", "Carpet (aka Loose Earth)"),
    ("SURFACE_MATERIAL_SNOW", "Snow", "Snow"),
]

ootEnumConveyorSpeed = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "None", "None"),
    ("0x01", "Slow", "Slow"),
    ("0x02", "Medium", "Medium"),
    ("0x03", "Fast", "Fast"),
]

enum_camera_crawlspace_stype = [
    ("Custom", "Custom", "Custom"),
    ("CAM_SET_CRAWLSPACE", "Crawlspace", "Crawlspace"),
]

ootEnumCameraSType = [
    ("Custom", "Custom", "Custom"),
    ("CAM_SET_NONE", "None", "None"),
    ("CAM_SET_NORMAL0", "Normal0", "Normal0"),
    ("CAM_SET_NORMAL1", "Normal1", "Normal1"),
    ("CAM_SET_DUNGEON0", "Dungeon0", "Dungeon0"),
    ("CAM_SET_DUNGEON1", "Dungeon1", "Dungeon1"),
    ("CAM_SET_NORMAL3", "Normal3", "Normal3"),
    ("CAM_SET_HORSE0", "Horse", "Horse"),
    ("CAM_SET_BOSS_GOMA", "Boss_gohma", "Boss_gohma"),
    ("CAM_SET_BOSS_DODO", "Boss_dodongo", "Boss_dodongo"),
    ("CAM_SET_BOSS_BARI", "Boss_barinade", "Boss_barinade"),
    ("CAM_SET_BOSS_FGANON", "Boss_phantom_ganon", "Boss_phantom_ganon"),
    ("CAM_SET_BOSS_BAL", "Boss_volvagia", "Boss_volvagia"),
    ("CAM_SET_BOSS_SHADES", "Boss_bongo", "Boss_bongo"),
    ("CAM_SET_BOSS_MOFA", "Boss_morpha", "Boss_morpha"),
    ("CAM_SET_TWIN0", "Twinrova_platform", "Twinrova_platform"),
    ("CAM_SET_TWIN1", "Twinrova_floor", "Twinrova_floor"),
    ("CAM_SET_BOSS_GANON1", "Boss_ganondorf", "Boss_ganondorf"),
    ("CAM_SET_BOSS_GANON2", "Boss_ganon", "Boss_ganon"),
    ("CAM_SET_TOWER0", "Tower_climb", "Tower_climb"),
    ("CAM_SET_TOWER1", "Tower_unused", "Tower_unused"),
    ("CAM_SET_FIXED0", "Market_balcony", "Market_balcony"),
    ("CAM_SET_FIXED1", "Chu_bowling", "Chu_bowling"),
    ("CAM_SET_CIRCLE0", "Pivot_crawlspace", "Pivot_crawlspace"),
    ("CAM_SET_CIRCLE2", "Pivot_shop_browsing", "Pivot_shop_browsing"),
    ("CAM_SET_CIRCLE3", "Pivot_in_front", "Pivot_in_front"),
    ("CAM_SET_PREREND0", "Prerend_fixed", "Prerend_fixed"),
    ("CAM_SET_PREREND1", "Prerend_pivot", "Prerend_pivot"),
    ("CAM_SET_PREREND3", "Prerend_side_scroll", "Prerend_side_scroll"),
    ("CAM_SET_DOOR0", "Door0", "Door0"),
    ("CAM_SET_DOORC", "Doorc", "Doorc"),
    ("CAM_SET_RAIL3", "Crawlspace", "Crawlspace"),
    ("CAM_SET_START0", "Start0", "Start0"),
    ("CAM_SET_START1", "Start1", "Start1"),
    ("CAM_SET_FREE0", "Free0", "Free0"),
    ("CAM_SET_FREE2", "Free2", "Free2"),
    ("CAM_SET_CIRCLE4", "Pivot_corner", "Pivot_corner"),
    ("CAM_SET_CIRCLE5", "Pivot_water_surface", "Pivot_water_surface"),
    ("CAM_SET_DEMO0", "Cs_0", "Cs_0"),
    ("CAM_SET_DEMO1", "Twisted_Hallway", "Twisted_Hallway"),
    ("CAM_SET_MORI1", "Forest_birds_eye", "Forest_birds_eye"),
    ("CAM_SET_ITEM0", "Slow_chest_cs", "Slow_chest_cs"),
    ("CAM_SET_ITEM1", "Item_unused", "Item_unused"),
    ("CAM_SET_DEMO3", "Cs_3", "Cs_3"),
    ("CAM_SET_DEMO4", "Cs_attention", "Cs_attention"),
    ("CAM_SET_UFOBEAN", "Bean_generic", "Bean_generic"),
    ("CAM_SET_LIFTBEAN", "Bean_lost_woods", "Bean_lost_woods"),
    ("CAM_SET_SCENE0", "Scene_unused", "Scene_unused"),
    ("CAM_SET_SCENE1", "Scene_transition", "Scene_transition"),
    ("CAM_SET_HIDAN1", "Fire_platform", "Fire_platform"),
    ("CAM_SET_HIDAN2", "Fire_staircase", "Fire_staircase"),
    ("CAM_SET_MORI2", "Forest_unused", "Forest_unused"),
    ("CAM_SET_MORI3", "Defeat_poe", "Defeat_poe"),
    ("CAM_SET_TAKO", "Big_octo", "Big_octo"),
    ("CAM_SET_SPOT05A", "Meadow_birds_eye", "Meadow_birds_eye"),
    ("CAM_SET_SPOT05B", "Meadow_unused", "Meadow_unused"),
    ("CAM_SET_HIDAN3", "Fire_birds_eye", "Fire_birds_eye"),
    ("CAM_SET_ITEM2", "Turn_around", "Turn_around"),
    ("CAM_SET_CIRCLE6", "Pivot_vertical", "Pivot_vertical"),
    ("CAM_SET_NORMAL2", "Normal2", "Normal2"),
    ("CAM_SET_FISHING", "Fishing", "Fishing"),
    ("CAM_SET_DEMOC", "Cs_c", "Cs_c"),
    ("CAM_SET_UO_FIBER", "Jabu_tentacle", "Jabu_tentacle"),
    ("CAM_SET_DUNGEON2", "Dungeon2", "Dungeon2"),
    ("CAM_SET_TEPPEN", "Directed_yaw", "Directed_yaw"),
    ("CAM_SET_CIRCLE7", "Pivot_from_side", "Pivot_from_side"),
    ("CAM_SET_NORMAL4", "Normal4", "Normal4"),
]

decomp_compat_map_CameraSType = {
    "CAM_SET_HORSE0": "CAM_SET_HORSE",
    "CAM_SET_BOSS_GOMA": "CAM_SET_BOSS_GOHMA",
    "CAM_SET_BOSS_DODO": "CAM_SET_BOSS_DODONGO",
    "CAM_SET_BOSS_BARI": "CAM_SET_BOSS_BARINADE",
    "CAM_SET_BOSS_FGANON": "CAM_SET_BOSS_PHANTOM_GANON",
    "CAM_SET_BOSS_BAL": "CAM_SET_BOSS_VOLVAGIA",
    "CAM_SET_BOSS_SHADES": "CAM_SET_BOSS_BONGO",
    "CAM_SET_BOSS_MOFA": "CAM_SET_BOSS_MORPHA",
    "CAM_SET_TWIN0": "CAM_SET_BOSS_TWINROVA_PLATFORM",
    "CAM_SET_TWIN1": "CAM_SET_BOSS_TWINROVA_FLOOR",
    "CAM_SET_BOSS_GANON1": "CAM_SET_BOSS_GANONDORF",
    "CAM_SET_BOSS_GANON2": "CAM_SET_BOSS_GANON",
    "CAM_SET_TOWER0": "CAM_SET_TOWER_CLIMB",
    "CAM_SET_TOWER1": "CAM_SET_TOWER_UNUSED",
    "CAM_SET_FIXED0": "CAM_SET_MARKET_BALCONY",
    "CAM_SET_FIXED1": "CAM_SET_CHU_BOWLING",
    "CAM_SET_CIRCLE0": "CAM_SET_PIVOT_CRAWLSPACE",
    "CAM_SET_CIRCLE2": "CAM_SET_PIVOT_SHOP_BROWSING",
    "CAM_SET_CIRCLE3": "CAM_SET_PIVOT_IN_FRONT",
    "CAM_SET_PREREND0": "CAM_SET_PREREND_FIXED",
    "CAM_SET_PREREND1": "CAM_SET_PREREND_PIVOT",
    "CAM_SET_PREREND3": "CAM_SET_PREREND_SIDE_SCROLL",
    "CAM_SET_RAIL3": "CAM_SET_CRAWLSPACE",
    "CAM_SET_CIRCLE4": "CAM_SET_PIVOT_CORNER",
    "CAM_SET_CIRCLE5": "CAM_SET_PIVOT_WATER_SURFACE",
    "CAM_SET_DEMO0": "CAM_SET_CS_0",
    "CAM_SET_DEMO1": "CAM_SET_CS_TWISTED_HALLWAY",
    "CAM_SET_MORI1": "CAM_SET_FOREST_BIRDS_EYE",
    "CAM_SET_ITEM0": "CAM_SET_SLOW_CHEST_CS",
    "CAM_SET_ITEM1": "CAM_SET_ITEM_UNUSED",
    "CAM_SET_DEMO3": "CAM_SET_CS_3",
    "CAM_SET_DEMO4": "CAM_SET_CS_ATTENTION",
    "CAM_SET_UFOBEAN": "CAM_SET_BEAN_GENERIC",
    "CAM_SET_LIFTBEAN": "CAM_SET_BEAN_LOST_WOODS",
    "CAM_SET_SCENE0": "CAM_SET_SCENE_UNUSED",
    "CAM_SET_SCENE1": "CAM_SET_SCENE_TRANSITION",
    "CAM_SET_HIDAN1": "CAM_SET_ELEVATOR_PLATFORM",
    "CAM_SET_HIDAN2": "CAM_SET_FIRE_STAIRCASE",
    "CAM_SET_MORI2": "CAM_SET_FOREST_UNUSED",
    "CAM_SET_MORI3": "CAM_SET_FOREST_DEFEAT_POE",
    "CAM_SET_TAKO": "CAM_SET_BIG_OCTO",
    "CAM_SET_SPOT05A": "CAM_SET_MEADOW_BIRDS_EYE",
    "CAM_SET_SPOT05B": "CAM_SET_MEADOW_UNUSED",
    "CAM_SET_HIDAN3": "CAM_SET_FIRE_BIRDS_EYE",
    "CAM_SET_ITEM2": "CAM_SET_TURN_AROUND",
    "CAM_SET_CIRCLE6": "CAM_SET_PIVOT_VERTICAL",
    "CAM_SET_DEMOC": "CAM_SET_CS_C",
    "CAM_SET_UO_FIBER": "CAM_SET_JABU_TENTACLE",
    "CAM_SET_TEPPEN": "CAM_SET_DIRECTED_YAW",
    "CAM_SET_CIRCLE7": "CAM_SET_PIVOT_FROM_SIDE",
}
