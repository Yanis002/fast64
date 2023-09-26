from dataclasses import dataclass, field
from mathutils import Vector
from ...utility import PluginError, indent


@dataclass
class CollisionPoly:
    indices: list[int]
    ignoreCamera: bool
    ignoreActor: bool
    ignoreProjectile: bool
    enableConveyor: bool
    normal: Vector
    dist: int
    type: int = None

    def getFlags_vIA(self):
        vertPart = self.indices[0] & 0x1FFF
        colPart = (1 if self.ignoreCamera else 0) + (2 if self.ignoreActor else 0) + (4 if self.ignoreProjectile else 0)
        return vertPart | (colPart << 13)

    def getFlags_vIB(self):
        vertPart = self.indices[1] & 0x1FFF
        conveyorPart = 1 if self.enableConveyor else 0
        return vertPart | (conveyorPart << 13)

    def getVIC(self):
        return self.indices[2] & 0x1FFF

    def getEntryC(self):
        if self.type is None:
            raise PluginError("ERROR: Type unset!")
        return (
            (indent + "{ ")
            + ", ".join(
                (
                    f"0x{self.type:04X}",
                    f"0x{self.getFlags_vIA():04X}",
                    f"0x{self.getFlags_vIB():04X}",
                    f"0x{self.getVIC():04X}",
                    ", ".join(f"COLPOLY_SNORMAL({val})" for val in self.normal),
                    f"{self.dist:6}",
                )
            )
            + " },"
        )


@dataclass
class SurfaceType:
    bgCamIndex: int
    exitIndex: int
    floorType: int
    unk18: int  # unused?
    wallType: int
    floorProperty: int
    isSoft: bool
    isHorseBlocked: bool

    material: int
    floorEffect: int
    lightSetting: int
    echo: int
    canHookshot: bool
    conveyorSpeed: int
    conveyorDirection: int
    isWallDamage: bool  # unk27

    conveyorKeepMomentum: bool
    useMacros: bool = True
    isSoftC: str = None
    isHorseBlockedC: str = None
    canHookshotC: str = None
    isWallDamageC: str = None

    def __post_init__(self):
        if self.conveyorKeepMomentum:
            self.conveyorSpeed += 4

        self.isSoftC = "1" if self.isSoft else "0"
        self.isHorseBlockedC = "1" if self.isHorseBlocked else "0"
        self.canHookshotC = "1" if self.canHookshot else "0"
        self.isWallDamageC = "1" if self.isWallDamage else "0"

    def getSurfaceType0(self):
        if self.useMacros:
            return (
                ("SURFACETYPE0(")
                + f"{self.bgCamIndex}, {self.exitIndex}, {self.floorType}, {self.unk18}, "
                + f"{self.wallType}, {self.floorProperty}, {self.isSoftC}, {self.isHorseBlockedC}"
                + ")"
            )
        else:
            return (
                (indent * 2 + "(")
                + " | ".join(
                    prop
                    for prop in [
                        f"(({self.isHorseBlockedC} & 1) << 31)",
                        f"(({self.isSoftC} & 1) << 30)",
                        f"(({self.floorProperty} & 0x0F) << 26)",
                        f"(({self.wallType} & 0x1F) << 21)",
                        f"(({self.unk18} & 0x07) << 18)",
                        f"(({self.floorType} & 0x1F) << 13)",
                        f"(({self.exitIndex} & 0x1F) << 8)",
                        f"({self.bgCamIndex} & 0xFF)",
                    ]
                )
                + ")"
            )

    def getSurfaceType1(self):
        if self.useMacros:
            return (
                ("SURFACETYPE1(")
                + f"{self.material}, {self.floorEffect}, {self.lightSetting}, {self.echo}, "
                + f"{self.canHookshotC}, {self.conveyorSpeed}, {self.conveyorDirection}, {self.isWallDamageC}"
                + ")"
            )
        else:
            return (
                (indent * 2 + "(")
                + " | ".join(
                    prop
                    for prop in [
                        f"(({self.isWallDamageC} & 1) << 27)",
                        f"(({self.conveyorDirection} & 0x3F) << 21)",
                        f"(({self.conveyorSpeed} & 0x07) << 18)",
                        f"(({self.canHookshotC} & 1) << 17)",
                        f"(({self.echo} & 0x3F) << 11)",
                        f"(({self.lightSetting} & 0x1F) << 6)",
                        f"(({self.floorEffect} & 0x03) << 4)",
                        f"({self.material} & 0x0F)",
                    ]
                )
                + ")"
            )

    def getEntryC(self):
        if self.useMacros:
            return indent + "{ " + self.getSurfaceType0() + ", " + self.getSurfaceType1() + " },"
        else:
            return (indent + "{\n") + self.getSurfaceType0() + ",\n" + self.getSurfaceType1() + ("\n" + indent + "},")


@dataclass
class BgCamFuncData:  # CameraPosData
    pos: tuple[int, int, int]
    rot: tuple[int, int, int]
    fov: int
    roomImageOverrideBgCamIndex: int


@dataclass
class CrawlspaceData:
    points: list[tuple[int, int, int]] = field(default_factory=list)
    arrayIndex: int = None

    def getDataEntriesC(self):
        return "".join(indent + "{ " + f"{point[0]:6}, {point[1]:6}, {point[2]:6}" + " },\n" for point in self.points)

    def getInfoEntryC(self, posDataName: str):
        return indent + "{ " + f"CAM_SET_CRAWLSPACE, 6, &{posDataName}[{self.arrayIndex}]" + " },\n"


@dataclass
class BgCamInfo:
    setting: str
    count: int
    arrayIndex: int
    hasPosData: bool
    bgCamFuncDataList: list[BgCamFuncData]

    def getDataEntriesC(self):
        source = ""

        if self.hasPosData:
            for camData in self.bgCamFuncDataList:
                source += (
                    (indent + "{ " + ", ".join(f"{p:6}" for p in camData.pos) + " },\n")
                    + (indent + "{ " + ", ".join(f"{r:6}" for r in camData.rot) + " },\n")
                    + (indent + "{ " + f"{camData.fov:6}, {camData.roomImageOverrideBgCamIndex:6}, {-1:6}" + " },\n")
                )

        return source

    def getInfoEntryC(self, posDataName: str):
        ptr = f"&{posDataName}[{self.arrayIndex}]" if self.hasPosData else "NULL"
        return indent + "{ " + f"{self.setting}, {self.count}, {ptr}" + " },\n"


@dataclass
class WaterBox:
    position: tuple[int, int, int]
    scale: float
    emptyDisplaySize: float

    # Properties
    bgCamIndex: int
    lightIndex: int
    roomIndex: int
    setFlag19: bool

    xMin: int = None
    ySurface: int = None
    zMin: int = None
    xLength: int = None
    zLength: int = None

    useMacros: bool = True
    setFlag19C: str = None
    roomIndexC: str = None

    def __post_init__(self):
        self.setFlag19C = "1" if self.setFlag19 else "0"
        self.roomIndexC = f"0x{self.roomIndex:02X}" if self.roomIndex == 0x3F else f"{self.roomIndex}"

        # The scale ordering is due to the fact that scaling happens AFTER rotation.
        # Thus the translation uses Y-up, while the scale uses Z-up.
        xMax = round(self.position[0] + self.scale[0] * self.emptyDisplaySize)
        zMax = round(self.position[2] + self.scale[1] * self.emptyDisplaySize)

        self.xMin = round(self.position[0] - self.scale[0] * self.emptyDisplaySize)
        self.ySurface = round(self.position[1] + self.scale[2] * self.emptyDisplaySize)
        self.zMin = round(self.position[2] - self.scale[1] * self.emptyDisplaySize)
        self.xLength = xMax - self.xMin
        self.zLength = zMax - self.zMin

    def getProperties(self):
        if self.useMacros:
            return f"WATERBOX_PROPERTIES({self.bgCamIndex}, {self.lightIndex}, {self.roomIndexC}, {self.setFlag19C})"
        else:
            return (
                "("
                + " | ".join(
                    prop
                    for prop in [
                        f"(({self.setFlag19C} & 1) << 19)",
                        f"(({self.roomIndexC} & 0x3F) << 13)",
                        f"(({self.lightIndex} & 0x1F) <<  8)",
                        f"(({self.bgCamIndex}) & 0xFF)",
                    ]
                )
                + ")"
            )

    def getEntryC(self):
        return (
            (indent + "{ ")
            + f"{self.xMin}, {self.ySurface}, {self.zMin}, {self.xLength}, {self.zLength}, "
            + self.getProperties()
            + " },"
        )


@dataclass
class Vertex:
    pos: tuple[int, int, int]

    def getEntryC(self):
        return indent + "{ " + ", ".join(f"{p:6}" for p in self.pos) + " },"