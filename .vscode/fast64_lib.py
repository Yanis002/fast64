from dataclasses import dataclass
from bpy.types import Object

from .oot_lib import (
    OOT_BoneLib,
    OOT_WorldLib,
    OOT_MaterialLib,
    OOT_SceneLib,
    OOT_ObjectLib,
    OOT_Properties,
    OOT_ObjectProperties,
)

from .sm64_lib import (
    SM64_BoneLib,
    SM64_WorldLib,
    SM64_MaterialLib,
    SM64_SceneLib,
    SM64_ObjectLib,
    SM64_CurveLib,
    SM64_Properties,
    SM64_BoneProperties,
    SM64_ObjectProperties,
)

from .f3d_lib import (
    F3D_WorldLib,
    F3D_MaterialLib,
    F3D_SceneLib,
    F3D_ObjectLib,
)


# render settings props
@dataclass
class Fast64RenderSettings_Properties:
    enableFogPreview: bool
    fogPreviewColor: list[float]
    ambientColor: list[float]
    lightColor: list[float]
    lightDirection: list[float]
    useWorldSpaceLighting: bool
    # Fog Preview is int because values reflect F3D values
    fogPreviewPosition: list[int]
    # Clipping planes are float because values reflect F3D values
    clippingPlanes: list[float]
    useObjectRenderPreview: bool
    # SM64
    sm64Area: "Object"
    # OOT
    ootSceneObject: "Object"
    ootSceneHeader: int
    ootForceTimeOfDay: bool
    ootLightIdx: int
    ootTime: float


# init props
@dataclass
class Fast64Settings_Properties:
    """Settings affecting exports for all games found in scene.fast64.settings"""

    version: int
    anim_range_choice: str


@dataclass
class Fast64_Properties:
    """
    Properties in scene.fast64.
    All new properties should be children of one of these three property groups.
    """

    sm64: SM64_Properties
    oot: OOT_Properties
    settings: Fast64Settings_Properties
    renderSettings: Fast64RenderSettings_Properties


@dataclass
class Fast64_BoneProperties:
    """
    Properties in bone.fast64 (bpy.types.Bone)
    All new bone properties should be children of this property group.
    """

    sm64: SM64_BoneProperties


@dataclass
class Fast64_ObjectProperties:
    """
    Properties in object.fast64 (bpy.types.Object)
    All new object properties should be children of this property group.
    """

    sm64: SM64_ObjectProperties
    oot: OOT_ObjectProperties


# main lib


@dataclass
class Fast64_ObjectLib(OOT_ObjectLib, SM64_ObjectLib, F3D_ObjectLib):
    fast64: Fast64_ObjectProperties


@dataclass
class Fast64_SceneLib(OOT_SceneLib, SM64_SceneLib, F3D_SceneLib):
    bsdf_conv_all: bool
    update_conv_all: bool
    rename_uv_maps: bool
    decomp_compatible: bool
    ignoreTextureRestrictions: bool
    fullTraceback: bool
    gameEditorMode: str
    saveTextures: bool
    generateF3DNodeGraph: bool
    exportHiddenGeometry: bool
    exportInlineF3D: bool
    blenderF3DScale: float

    fast64: Fast64_Properties


@dataclass
class Fast64_MaterialLib(OOT_MaterialLib, SM64_MaterialLib, F3D_MaterialLib):
    pass


@dataclass
class Fast64_WorldLib(OOT_WorldLib, SM64_WorldLib, F3D_WorldLib):
    pass


@dataclass
class Fast64_BoneLib(OOT_BoneLib, SM64_BoneLib):
    fast64: Fast64_BoneProperties


@dataclass
class Fast64_CurveLib(SM64_CurveLib):
    pass
