from dataclasses import dataclass
from typing import Collection
from bpy.types import Object, Camera, Material, ImageTexture
from mathutils import Vector
from .f3d_lib import TextureProperty


# object props
@dataclass
class WarpNodeProperty:
    warpType: str
    warpID: str
    destLevelEnum: str
    destLevel: str
    destArea: str
    destNode: str
    warpFlags: str
    warpFlagEnum: str
    instantOffset: list[int]
    instantWarpObject1: "Object"
    instantWarpObject2: "Object"
    useOffsetObjects: bool
    expand: bool

    def uses_area_nodes(self) -> bool:
        pass

    def calc_offsets_from_objects(self, reverse=False) -> "Vector":
        pass

    def to_c(self) -> str:
        pass


@dataclass
class StarGetCutscenesProperty:
    star1_option: str
    star2_option: str
    star3_option: str
    star4_option: str
    star5_option: str
    star6_option: str
    star7_option: str
    star1_value: int
    star2_value: int
    star3_value: int
    star4_value: int
    star5_value: int
    star6_value: int
    star7_value: int

    def value(self) -> str:
        pass

    def draw(self, layout):
        pass


@dataclass
class PuppycamProperty:
    puppycamVolumeFunction: str
    puppycamVolumePermaswap: bool
    puppycamUseEmptiesForPos: bool
    puppycamCamera: "Object"
    puppycamFOV: float
    puppycamMode: str
    puppycamType: str
    puppycamCamPos: str
    puppycamCamFocus: str
    puppycamUseFlags: bool
    NC_FLAG_XTURN: bool
    NC_FLAG_YTURN: bool
    NC_FLAG_ZOOM: bool
    NC_FLAG_8D: bool
    NC_FLAG_4D: bool
    NC_FLAG_2D: bool
    NC_FLAG_FOCUSX: bool
    NC_FLAG_FOCUSY: bool
    NC_FLAG_FOCUSZ: bool
    NC_FLAG_POSX: bool
    NC_FLAG_POSY: bool
    NC_FLAG_POSZ: bool
    NC_FLAG_COLLISION: bool
    NC_FLAG_SLIDECORRECT: bool


@dataclass
class SM64_GeoASMProperties:
    name: str
    func: str
    param: str

    @staticmethod
    def upgrade_object(obj: "Object"):
        pass


@dataclass
class SM64_AreaProperties:
    name: str
    disable_background: bool


@dataclass
class SM64_LevelProperties:
    name: str
    backgroundID: str
    backgroundSegment: str


@dataclass
class SM64_GameObjectProperties:
    name: str
    bparams: str
    use_individual_params: bool
    bparam1: str
    bparam2: str
    bparam3: str
    bparam4: str

    @staticmethod
    def upgrade_object(obj):
        pass

    def get_combined_bparams(self) -> str:
        pass

    def get_behavior_params(self) -> str:
        pass


@dataclass
class SM64_SegmentProperties:
    seg5_load_custom: str
    seg5_group_custom: str
    seg6_load_custom: str
    seg6_group_custom: str
    seg5_enum: str
    seg6_enum: str

    def draw(self, layout):
        pass

    def jump_link_from_enum(self, grp) -> str:
        pass

    @property
    def seg5(self) -> str:
        pass

    @property
    def seg6(self) -> str:
        pass

    @property
    def group5(self) -> str:
        pass

    @property
    def group6(self) -> str:
        pass


@dataclass
class SM64_ObjectProperties:
    version: int
    cur_version: int

    geo_asm: SM64_GeoASMProperties
    level: SM64_LevelProperties
    area: SM64_AreaProperties
    game_object: SM64_GameObjectProperties
    segment_loads: SM64_SegmentProperties

    @staticmethod
    def upgrade_changed_props():
        pass


# geolayout bone props
@dataclass
class MaterialPointerProperty:
    material: "Material"


@dataclass
class SwitchOptionProperty:
    switchType: str
    optionArmature: "Object"
    materialOverride: "Material"
    materialOverrideType: str
    specificOverrideArray: Collection[MaterialPointerProperty]
    specificIgnoreArray: Collection[MaterialPointerProperty]
    overrideDrawLayer: bool
    drawLayer: str
    expand: bool


@dataclass
class SM64_BoneProperties:
    version: int
    custom_geo_cmd_macro: str
    custom_geo_cmd_args: str


# init props
@dataclass
class SM64_Properties:
    """Global SM64 Scene Properties found under scene.fast64.sm64"""

    version: int
    cur_version: int

    # UI Selection
    showImportingMenus: bool
    exportType: str
    goal: str

    @staticmethod
    def upgrade_changed_props():
        pass


# lib


@dataclass
class SM64_CurveLib:
    sm64_spline_type: str


@dataclass
class SM64_BoneLib:
    geo_cmd: str
    draw_layer: str
    # Scale
    geo_scale: float
    # Function, HeldObject, Switch
    # 8027795C for HeldObject
    geo_func: str
    # Function
    func_param: int
    # TranslateRotate
    field_layout: str
    # Shadow
    shadow_type: str
    shadow_solidity: float
    shadow_scale: int
    # StartRenderArea
    culling_radius: float
    switch_options: Collection[SwitchOptionProperty]


@dataclass
class SM64_WorldLib:
    draw_layer_0_cycle_1: str
    draw_layer_0_cycle_2: str
    draw_layer_1_cycle_1: str
    draw_layer_1_cycle_2: str
    draw_layer_2_cycle_1: str
    draw_layer_2_cycle_2: str
    draw_layer_3_cycle_1: str
    draw_layer_3_cycle_2: str
    draw_layer_4_cycle_1: str
    draw_layer_4_cycle_2: str
    draw_layer_5_cycle_1: str
    draw_layer_5_cycle_2: str
    draw_layer_6_cycle_1: str
    draw_layer_6_cycle_2: str
    draw_layer_7_cycle_1: str
    draw_layer_7_cycle_2: str


@dataclass
class SM64_MaterialLib:
    collision_type: str
    collision_type_simple: str
    collision_custom: str
    collision_all_options: bool
    use_collision_param: bool
    collision_param: str


@dataclass
class SM64_SceneLib:
    animStartImport: str
    animExportStart: str
    animExportEnd: str
    isDMAImport: bool
    isDMAExport: bool
    DMAEntryAddress: str
    DMAStartAddress: str
    levelAnimImport: str
    levelAnimExport: str
    loopAnimation: bool
    setAnimListIndex: bool
    overwrite_0x28: bool
    addr_0x27: str
    addr_0x28: str
    animExportPath: str
    animOverwriteDMAEntry: bool
    animInsertableBinaryPath: str
    animIsSegPtr: bool
    animIsAnimList: bool
    animListIndexImport: int
    animListIndexExport: int
    animName: str
    animGroupName: str
    animWriteHeaders: bool
    animCustomExport: bool
    animExportHeaderType: str
    animLevelName: str
    animLevelOption: str
    colExportPath: str
    colExportLevel: str
    addr_0x2A: str
    set_addr_0x2A: bool
    colStartAddr: str
    colEndAddr: str
    colIncludeChildren: bool
    colInsertableBinaryPath: str
    colExportRooms: bool
    colName: str
    colCustomExport: bool
    colExportHeaderType: str
    colGroupName: str
    colLevelName: str
    colLevelOption: str
    DLImportStart: str
    levelDLImport: str
    isSegmentedAddrDLImport: bool
    DLExportStart: str
    DLExportEnd: str
    levelDLExport: str
    DLExportGeoPtr: str
    overwriteGeoPtr: bool
    DLExportPath: str
    DLExportisStatic: bool
    DLDefinePath: str
    DLUseBank0: bool
    DLRAMAddr: str
    DLTexDir: str
    DLSeparateTextureDef: bool
    DLincludeChildren: bool
    DLInsertableBinaryPath: str
    DLName: str
    DLCustomExport: bool
    DLExportHeaderType: str
    DLGroupName: str
    DLLevelName: str
    DLLevelOption: str
    texrect: TextureProperty
    texrectImageTexture: "ImageTexture"
    TexRectExportPath: str
    TexRectTexDir: str
    TexRectName: str
    TexRectCustomExport: bool
    TexRectExportType: str
    geoImportAddr: str
    generateArmature: bool
    levelGeoImport: str
    ignoreSwitch: bool
    levelGeoExport: str
    geoExportStart: str
    geoExportEnd: str
    overwriteModelLoad: bool
    modelLoadLevelScriptCmd: str
    modelID: str
    textDumpGeo: bool
    textDumpGeoPath: str
    geoExportPath: str
    geoUseBank0: bool
    geoRAMAddr: str
    geoTexDir: str
    geoSeparateTextureDef: bool
    geoInsertableBinaryPath: str
    geoIsSegPtr: bool
    geoName: str
    geoGroupName: str
    geoExportHeaderType: str
    geoCustomExport: bool
    geoLevelName: str
    geoLevelOption: str
    replaceStarRefs: bool
    replaceTransparentStarRefs: bool
    replaceCapRefs: bool
    modifyOldGeo: bool
    geoStructName: str
    levelName: str
    levelOption: str
    levelExportPath: str
    levelCustomExport: bool
    importRom: str
    exportRom: str
    outputRom: str
    extendBank4: bool
    convertibleAddr: str
    levelConvert: str
    refreshVer: str
    disableScroll: bool
    blenderToSM64Scale: float
    decompPath: str
    compressionFormat: str


@dataclass
class SM64_ObjectLib:
    sm64_water_box: str
    sm64_special_preset: str
    room_num: int
    geo_cmd_static: str
    draw_layer_static: str
    use_render_area: bool
    culling_radius: float
    add_shadow: bool
    shadow_type: str
    shadow_solidity: float
    shadow_scale: int
    add_func: bool
    use_render_range: bool
    render_range: list[float]
    scaleFromGeolayout: bool
    # Used during object duplication on export
    original_name: str
    puppycamProp: PuppycamProperty
    sm64_model_enum: str
    sm64_macro_enum: str
    sm64_special_enum: str
    sm64_behaviour_enum: str
    sm64_obj_type: str
    sm64_obj_model: str
    sm64_obj_preset: str
    sm64_obj_behaviour: str
    sm64_obj_mario_start_area: str
    whirpool_index: str
    whirpool_condition: str
    whirpool_strength: str
    waterBoxType: str
    sm64_obj_use_act1: bool
    sm64_obj_use_act2: bool
    sm64_obj_use_act3: bool
    sm64_obj_use_act4: bool
    sm64_obj_use_act5: bool
    sm64_obj_use_act6: bool
    sm64_obj_set_bparam: bool
    sm64_obj_set_yaw: bool
    useBackgroundColor: bool
    background: str
    backgroundColor: list[float]
    screenPos: list[int]
    screenSize: list[int]
    useDefaultScreenRect: bool
    clipPlanes: list[int]
    area_fog_color: list[float]
    area_fog_position: list[float]
    areaOverrideBG: bool
    areaBGColor: list[float]
    camOption: str
    camType: str
    envOption: str
    envType: str
    fov: float
    dynamicFOV: bool
    cameraVolumeFunction: str
    cameraVolumeGlobal: bool
    starGetCutscenes: StarGetCutscenesProperty
    acousticReach: str
    echoLevel: str
    zoomOutOnPause: bool
    areaIndex: int
    music_preset: str
    music_seq: str
    noMusic: bool
    terrain_type: str
    terrainEnum: str
    musicSeqEnum: str
    areaCamera: "Camera"
    warpNodes: WarpNodeProperty
    showStartDialog: bool
    startDialog: str
    actSelectorIgnore: bool
    setAsStartLevel: bool
    switchFunc: str
    switchParam: int
    useDLReference: bool
    dlReference: str
    geoReference: str
    customGeoCommand: str
    customGeoCommandArgs: str
    enableRoomSwitch: bool
