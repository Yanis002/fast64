from dataclasses import dataclass
from typing import Collection
from bpy.types import UILayout, Image, Object, Light


# skeleton props


@dataclass
class OOTDynamicTransformProperty:
    billboard: bool

    def draw_props(self, layout: "UILayout"):
        pass


@dataclass
class OOTBoneProperty:
    boneType: str
    dynamicTransform: OOTDynamicTransformProperty
    customDLName: str

    def draw_props(self, layout: "UILayout"):
        pass


@dataclass
class OOTSkeletonProperty:
    LOD: "Object"

    def draw_props(self, layout: "UILayout"):
        pass


@dataclass
class OOTSkeletonExportSettings:
    isCustomFilename: bool
    filename: str
    mode: str
    folder: str
    customPath: str
    isCustom: bool
    removeVanillaData: bool
    actorOverlayName: str
    flipbookUses2DArray: bool
    flipbookArrayIndex2D: int
    customAssetIncludeDir: str
    optimize: bool

    def draw_props(self, layout: "UILayout"):
        pass


@dataclass
class OOTSkeletonImportSettings:
    mode: str
    applyRestPose: bool
    name: str
    folder: str
    customPath: str
    isCustom: bool
    removeDoubles: bool
    importNormals: bool
    drawLayer: str
    actorOverlayName: str
    flipbookUses2DArray: bool
    flipbookArrayIndex2D: int
    autoDetectActorScale: bool
    actorScale: float

    def draw_props(self, layout: "UILayout"):
        pass


# f3d props
@dataclass
class OOTDLExportSettings:
    isCustomFilename: bool
    filename: str
    folder: str
    customPath: str
    isCustom: bool
    removeVanillaData: bool
    drawLayer: str
    actorOverlayName: str
    flipbookUses2DArray: bool
    flipbookArrayIndex2D: int
    customAssetIncludeDir: str

    def draw_props(self, layout: "UILayout"):
        pass


@dataclass
class OOTDLImportSettings:
    name: str
    folder: str
    customPath: str
    isCustom: bool
    removeDoubles: bool
    importNormals: bool
    drawLayer: str
    actorOverlayName: str
    flipbookUses2DArray: bool
    flipbookArrayIndex2D: int
    autoDetectActorScale: bool
    actorScale: float

    def draw_props(self, layout: "UILayout"):
        pass


@dataclass
class OOTDynamicMaterialDrawLayerProperty:
    segment8: bool
    segment9: bool
    segmentA: bool
    segmentB: bool
    segmentC: bool
    segmentD: bool
    customCall0: bool
    customCall0_seg: str
    customCall1: bool
    customCall1_seg: str

    def key(self) -> tuple[bool, bool, bool, bool, bool, bool, str | None, str | None]:
        pass

    def draw_props(self, layout: "UILayout", suffix: str):
        pass


# The reason these are separate is for the case when the user changes the material draw layer, but not the
# dynamic material calls. This could cause crashes which would be hard to detect.
@dataclass
class OOTDynamicMaterialProperty:
    opaque: OOTDynamicMaterialDrawLayerProperty
    transparent: OOTDynamicMaterialDrawLayerProperty

    def key(
        self,
    ) -> tuple[
        tuple[bool, bool, bool, bool, bool, bool, str | None, str | None],
        tuple[bool, bool, bool, bool, bool, bool, str | None, str | None],
    ]:
        pass

    def draw_props(self, layout: "UILayout", mat: "Object", drawLayer: str):
        pass


@dataclass
class OOTDefaultRenderModesProperty:
    expandTab: bool
    opaqueCycle1: str
    opaqueCycle2: str
    transparentCycle1: str
    transparentCycle2: str
    overlayCycle1: str
    overlayCycle2: str

    def draw_props(self, layout: "UILayout"):
        pass


# cutscene props


# Perhaps this should have been called something like OOTCSParentPropertyType,
# but now it needs to keep the same name to not break existing scenes which use
# the cutscene system.
@dataclass
class OOTCSProperty:
    propName: str
    attrName: str
    subprops: list[str]
    expandTab: bool
    startFrame: int
    endFrame: int

    def getName(self) -> str:
        pass

    def filterProp(self, name, listProp) -> bool:
        pass

    def filterName(self, name, listProp) -> str:
        pass

    def draw(self, layout, listProp, listIndex, cmdIndex, objName, collectionType):
        pass


@dataclass
class OOTCSTextboxProperty(OOTCSProperty):
    textboxType: str
    messageId: str
    ocarinaSongAction: str
    type: str
    topOptionBranch: str
    bottomOptionBranch: str
    ocarinaMessageId: str


@dataclass
class OOTCSLightingProperty(OOTCSProperty):
    index: int


@dataclass
class OOTCSTimeProperty(OOTCSProperty):
    hour: int
    minute: int


@dataclass
class OOTCSBGMProperty(OOTCSProperty):
    value: str


@dataclass
class OOTCSMiscProperty(OOTCSProperty):
    operation: int


@dataclass
class OOTCS0x09Property(OOTCSProperty):
    unk2: str
    unk3: str
    unk4: str


@dataclass
class OOTCSUnkProperty(OOTCSProperty):
    unk1: str
    unk2: str
    unk3: str
    unk4: str
    unk5: str
    unk6: str
    unk7: str
    unk8: str
    unk9: str
    unk10: str
    unk11: str
    unk12: str


@dataclass
class OOTCSListProperty:
    expandTab: bool

    listType: str
    textbox: Collection[OOTCSTextboxProperty]
    lighting: Collection[OOTCSLightingProperty]
    time: Collection[OOTCSTimeProperty]
    bgm: Collection[OOTCSBGMProperty]
    misc: Collection[OOTCSMiscProperty]
    nine: Collection[OOTCS0x09Property]
    unk: Collection[OOTCSUnkProperty]

    unkType: str
    fxType: str
    fxStartFrame: int
    fxEndFrame: int

    def draw_props(self, layout: "UILayout", listIndex: int, objName: str, collectionType: str):
        pass


@dataclass
class OOTCutsceneProperty:
    csEndFrame: int
    csWriteTerminator: bool
    csTermIdx: int
    csTermStart: int
    csTermEnd: int
    csLists: Collection[OOTCSListProperty]

    def draw_props(self, layout: "UILayout", obj: "Object"):
        pass


# collision props
@dataclass
class OOTCollisionExportSettings:
    isCustomFilename: bool
    filename: str
    exportPath: str
    exportLevel: str
    includeChildren: bool
    levelName: str
    customExport: bool
    folder: str

    def draw_props(self, layout: "UILayout"):
        pass


@dataclass
class OOTCameraPositionProperty:
    index: int
    bgImageOverrideIndex: int
    camSType: str
    camSTypeCustom: str
    hasPositionData: bool

    def draw_props(self, layout: "UILayout", cameraObj: "Object"):
        pass


@dataclass
class OOTMaterialCollisionProperty:
    expandTab: bool

    ignoreCameraCollision: bool
    ignoreActorCollision: bool
    ignoreProjectileCollision: bool

    eponaBlock: bool
    decreaseHeight: bool
    floorSettingCustom: str
    floorSetting: str
    wallSettingCustom: str
    wallSetting: str
    floorPropertyCustom: str
    floorProperty: str
    exitID: int
    cameraID: int
    isWallDamage: bool
    conveyorOption: str
    conveyorRotation: float
    conveyorSpeed: str
    conveyorSpeedCustom: str
    conveyorKeepMomentum: bool
    hookshotable: bool
    echo: str
    lightingSetting: int
    terrainCustom: str
    terrain: str
    soundCustom: str
    sound: str

    def draw_props(self, layout: "UILayout"):
        pass


@dataclass
class OOTWaterBoxProperty:
    lighting: int
    camera: int
    flag19: bool

    def draw_props(self, layout: "UILayout"):
        pass


# animation props
@dataclass
class OOTAnimExportSettingsProperty:
    isCustomFilename: bool
    filename: str
    isCustom: bool
    customPath: str
    folderName: str
    isLink: bool

    def draw_props(self, layout: "UILayout"):
        pass


@dataclass
class OOTAnimImportSettingsProperty:
    isCustom: bool
    customPath: str
    folderName: str
    isLink: bool
    animName: str

    def draw_props(self, layout: "UILayout"):
        pass


@dataclass
class OOTLinkTextureAnimProperty:
    eyes: int
    mouth: int

    def draw_props(self, layout: "UILayout"):
        pass


# scene props
@dataclass
class OOTSceneCommon:
    ootEnumBootMode: list[tuple[str, str, str]]

    def isSceneObj(self, obj) -> bool:
        pass


@dataclass
class OOTSceneProperties:
    write_dummy_room_list: bool


@dataclass
class OOTExitProperty:
    expandTab: bool

    exitIndex: str
    exitIndexCustom: str

    # These are used when adding an entry to gEntranceTable
    scene: str
    sceneCustom: str

    # These are used when adding an entry to gEntranceTable
    continueBGM: bool
    displayTitleCard: bool
    fadeInAnim: str
    fadeInAnimCustom: str
    fadeOutAnim: str
    fadeOutAnimCustom: str

    def draw_props(self, layout: "UILayout", index: int, headerIndex: int, objName: str):
        pass


@dataclass
class OOTLightProperty:
    ambient: list[float]
    useCustomDiffuse0: bool
    useCustomDiffuse1: bool
    diffuse0: list[float]
    diffuse1: list[float]
    diffuse0Custom: "Light"
    diffuse1Custom: "Light"
    fogColor: list[float]
    fogNear: int
    transitionSpeed: int
    fogFar: int
    expandTab: bool

    def draw_props(
        self, layout: "UILayout", name: str, showExpandTab: bool, index: int, sceneHeaderIndex: int, objName: str
    ):
        pass


@dataclass
class OOTLightGroupProperty:
    expandTab: bool
    menuTab: str
    dawn: OOTLightProperty
    day: OOTLightProperty
    dusk: OOTLightProperty
    night: OOTLightProperty
    defaultsSet: bool

    def draw_props(self, layout: "UILayout"):
        pass


@dataclass
class OOTSceneTableEntryProperty:
    drawConfig: str
    drawConfigCustom: str
    hasTitle: bool

    def draw_props(self, layout: "UILayout"):
        pass


@dataclass
class OOTExtraCutsceneProperty:
    csObject: "Object"


@dataclass
class OOTSceneHeaderProperty:
    expandTab: bool
    usePreviousHeader: bool

    globalObject: str
    globalObjectCustom: str
    naviCup: str
    naviCupCustom: str

    skyboxID: str
    skyboxIDCustom: str
    skyboxCloudiness: str
    skyboxCloudinessCustom: str
    skyboxLighting: str
    skyboxLightingCustom: str

    mapLocation: str
    mapLocationCustom: str
    cameraMode: str
    cameraModeCustom: str

    musicSeq: str
    musicSeqCustom: str
    nightSeq: str
    nightSeqCustom: str
    audioSessionPreset: str
    audioSessionPresetCustom: str

    timeOfDayLights: OOTLightGroupProperty
    lightList: Collection[OOTLightProperty]
    exitList: Collection[OOTExitProperty]

    writeCutscene: bool
    csWriteType: str
    csWriteCustom: str
    csWriteObject: "Object"

    # These properties are for the deprecated "Embedded" cutscene type. They have
    # not been removed as doing so would break any existing scenes made with this
    # type of cutscene data.
    csEndFrame: int
    csWriteTerminator: bool
    csTermIdx: int
    csTermStart: int
    csTermEnd: int
    csLists: Collection[OOTCSListProperty]

    extraCutscenes: Collection[OOTExtraCutsceneProperty]

    sceneTableEntry: OOTSceneTableEntryProperty

    menuTab: str
    altMenuTab: str

    appendNullEntrance: bool

    def draw_props(self, layout: "UILayout", dropdownLabel: str, headerIndex: int, objName: str):
        pass


@dataclass
class OOTAlternateSceneHeaderProperty:
    childNightHeader: OOTSceneHeaderProperty
    adultDayHeader: OOTSceneHeaderProperty
    adultNightHeader: OOTSceneHeaderProperty
    cutsceneHeaders: Collection[OOTSceneHeaderProperty]

    headerMenuTab: str
    currentCutsceneIndex: int

    def draw_props(self, layout: "UILayout", objName: str):
        pass


@dataclass
class OOTBootupSceneOptions:
    bootToScene: bool
    overrideHeader: bool
    headerOption: str
    spawnIndex: int
    newGameOnly: bool
    newGameName: str
    bootMode: str

    # see src/code/z_play.c:Play_Init() - can't access more than 16 cutscenes?
    cutsceneIndex: int

    def draw_props(self, layout: "UILayout"):
        pass


@dataclass
class OOTRemoveSceneSettingsProperty:
    name: str
    subFolder: str
    customExport: bool
    option: str

    def draw_props(self, layout: "UILayout"):
        pass


@dataclass
class OOTExportSceneSettingsProperty:
    name: str
    subFolder: str
    exportPath: str
    customExport: bool
    singleFile: bool
    option: str

    def draw_props(self, layout: "UILayout"):
        pass


@dataclass
class OOTImportSceneSettingsProperty:
    name: str
    subFolder: str
    destPath: str
    isCustomDest: bool
    includeMesh: bool
    includeCollision: bool
    includeActors: bool
    includeCullGroups: bool
    includeLights: bool
    includeCameras: bool
    includePaths: bool
    includeWaterBoxes: bool
    option: str

    def draw_props(self, layout: "UILayout", sceneOption: str):
        pass


# room props


@dataclass
class OOTObjectProperty:
    expandTab: bool
    objectKey: str
    objectIDCustom: str

    @staticmethod
    def upgrade_object(obj):
        pass

    def draw_props(self, layout: "UILayout", headerIndex: int, index: int, objName: str):
        pass


@dataclass
class OOTBGProperty:
    image: "Image"
    # camera: int
    otherModeFlags: str

    def draw_props(self, layout: "UILayout", index: int, objName: str, isMulti: bool):
        pass


@dataclass
class OOTRoomHeaderProperty:
    expandTab: bool
    menuTab: str
    altMenuTab: str
    usePreviousHeader: bool

    roomIndex: int
    roomBehaviour: str
    roomBehaviourCustom: str
    disableWarpSongs: bool
    showInvisibleActors: bool
    linkIdleMode: str
    linkIdleModeCustom: str
    roomIsHot: bool

    useCustomBehaviourX: bool
    useCustomBehaviourY: bool

    customBehaviourX: str

    customBehaviourY: str

    setWind: bool
    windVector: list[int]
    windStrength: int

    leaveTimeUnchanged: bool
    timeHours: int  # 0xFFFE
    timeMinutes: int
    timeSpeed: float

    disableSkybox: bool
    disableSunMoon: bool

    echo: str

    objectList: Collection[OOTObjectProperty]

    roomShape: str
    defaultCullDistance: int
    bgImageList: Collection[OOTBGProperty]
    bgImageTab: bool

    def drawBGImageList(self, layout: "UILayout", objName: str):
        pass

    def draw_props(self, layout: "UILayout", dropdownLabel: str, headerIndex: int, objName: str):
        pass


@dataclass
class OOTAlternateRoomHeaderProperty:
    childNightHeader: OOTRoomHeaderProperty
    adultDayHeader: OOTRoomHeaderProperty
    adultNightHeader: OOTRoomHeaderProperty
    cutsceneHeaders: Collection[OOTRoomHeaderProperty]

    headerMenuTab: str
    currentCutsceneIndex: int

    def draw_props(self, layout: "UILayout", objName: str):
        pass


# actor props


@dataclass
class OOTActorHeaderItemProperty:
    headerIndex: int
    expandTab: bool

    def draw_props(
        self,
        layout: "UILayout",
        propUser: str,
        index: int,
        altProp: OOTAlternateSceneHeaderProperty | OOTAlternateRoomHeaderProperty,
        objName: str,
    ):
        pass


@dataclass
class OOTActorHeaderProperty:
    sceneSetupPreset: str
    childDayHeader: bool
    childNightHeader: bool
    adultDayHeader: bool
    adultNightHeader: bool
    cutsceneHeaders: Collection[OOTActorHeaderItemProperty]

    def checkHeader(self, index: int) -> bool:
        pass

    def draw_props(
        self,
        layout: "UILayout",
        propUser: str,
        altProp: OOTAlternateSceneHeaderProperty | OOTAlternateRoomHeaderProperty,
        objName: str,
    ):
        pass


@dataclass
class OOTActorProperty:
    actorID: str
    actorIDCustom: str
    actorParam: str
    rotOverride: bool
    rotOverrideX: str
    rotOverrideY: str
    rotOverrideZ: str
    headerSettings: OOTActorHeaderProperty

    def draw_props(self, layout: "UILayout", altRoomProp: OOTAlternateRoomHeaderProperty, objName: str):
        pass


@dataclass
class OOTTransitionActorProperty:
    roomIndex: int
    cameraTransitionFront: str
    cameraTransitionFrontCustom: str
    cameraTransitionBack: str
    cameraTransitionBackCustom: str
    dontTransition: bool

    actor: OOTActorProperty

    def draw_props(
        self, layout: "UILayout", altSceneProp: OOTAlternateSceneHeaderProperty, roomObj: "Object", objName: str
    ):
        pass


@dataclass
class OOTEntranceProperty:
    # This is also used in entrance list, and roomIndex is obtained from the room this empty is parented to.
    spawnIndex: int
    customActor: bool
    actor: OOTActorProperty

    def draw_props(
        self, layout: "UILayout", obj: "Object", altSceneProp: OOTAlternateSceneHeaderProperty, objName: str
    ):
        pass


# spline props
@dataclass
class OOTSplineProperty:
    splineType: str
    index: int  # only used for crawlspace, not path
    headerSettings: OOTActorHeaderProperty
    camSType: str
    camSTypeCustom: str

    def draw_props(self, layout: "UILayout", altSceneProp: OOTAlternateSceneHeaderProperty, objName: str):
        pass


# props panel main
@dataclass
class OOT_ObjectProperties:
    scene: OOTSceneProperties

    @staticmethod
    def upgrade_changed_props():
        pass


@dataclass
class OOTCullGroupProperty:
    sizeControlsCull: bool
    manualRadius: int

    def draw_props(self, layout: "UILayout"):
        pass


# init
class OOT_Properties:
    """Global OOT Scene Properties found under scene.fast64.oot"""

    version: int
    hackerFeaturesEnabled: bool
    headerTabAffectsVisibility: bool
    bootupSceneOptions: OOTBootupSceneOptions
    DLExportSettings: OOTDLExportSettings
    DLImportSettings: OOTDLImportSettings
    skeletonExportSettings: OOTSkeletonExportSettings
    skeletonImportSettings: OOTSkeletonImportSettings
    animExportSettings: OOTAnimExportSettingsProperty
    animImportSettings: OOTAnimImportSettingsProperty
    collisionExportSettings: OOTCollisionExportSettings


# lib


@dataclass
class OOT_BoneLib:
    ootDefaultRenderModes: OOTDefaultRenderModesProperty
    ootBone: OOTBoneProperty


@dataclass
class OOT_WorldLib:
    ootDefaultRenderModes: OOTDefaultRenderModesProperty


@dataclass
class OOT_MaterialLib:
    ootCollisionProperty: OOTMaterialCollisionProperty
    ootMaterial: OOTDynamicMaterialProperty


@dataclass
class OOT_SceneLib:
    ootSceneExportObj: "Object"
    ootSceneExportSettings: OOTExportSceneSettingsProperty
    ootSceneImportSettings: OOTImportSceneSettingsProperty
    ootSceneRemoveSettings: OOTRemoveSceneSettingsProperty
    ootAnimIsCustomExport: bool
    ootAnimExportCustomPath: str
    ootAnimExportFolderName: str
    ootAnimIsCustomImport: bool
    ootAnimImportCustomPath: str
    ootAnimImportFolderName: str
    ootAnimSkeletonName: str
    ootAnimName: str
    ootCutsceneExportPath: str
    ootBlenderScale: float
    ootDecompPath: str
    ootActiveHeaderLock: bool


@dataclass
class OOT_ObjectLib:
    ootEmptyType: str
    ootActorProperty: OOTActorProperty
    ootTransitionActorProperty: OOTTransitionActorProperty
    ootEntranceProperty: OOTEntranceProperty
    ootRoomHeader: OOTRoomHeaderProperty
    ootAlternateRoomHeaders: OOTAlternateRoomHeaderProperty
    ootSceneHeader: OOTSceneHeaderProperty
    ootAlternateSceneHeaders: OOTAlternateSceneHeaderProperty
    ootLinkTextureAnim: OOTLinkTextureAnimProperty
    ootCameraPositionProperty: OOTCameraPositionProperty
    ootWaterBoxProperty: OOTWaterBoxProperty
    ootCutsceneProperty: OOTCutsceneProperty
    ootDrawLayer: str
    ootObjectMenu: str
    ootActorScale: float
    ootSkeleton: OOTSkeletonProperty
    ootSplineProperty: OOTSplineProperty
    ootCullGroupProperty: OOTCullGroupProperty
