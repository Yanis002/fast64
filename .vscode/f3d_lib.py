from dataclasses import dataclass
from typing import Collection
from bpy.types import Image, Light, Material


@dataclass
class DrawLayerProperty:
    sm64: str
    oot: str

    def key(self):
        return (self.sm64, self.oot)


@dataclass
class TextureFieldProperty:
    clamp: bool
    mirror: bool
    low: float
    high: float
    mask: int
    shift: int

    def key(self) -> tuple[bool, bool, int, int, int, int]:
        pass


@dataclass
class SetTileSizeScrollProperty:
    s: int
    t: int
    interval: int

    def key(self) -> tuple[int, int, int]:
        pass


@dataclass
class TextureProperty:
    tex: "Image"
    tex_format: str
    ci_format: str
    S: TextureFieldProperty
    T: TextureFieldProperty

    use_tex_reference: bool
    tex_reference: str
    tex_reference_size: list[int]
    pal_reference: str
    pal_reference_size: int

    menu: bool
    tex_set: bool
    autoprop: bool
    tile_scroll: SetTileSizeScrollProperty

    def get_tex_size(self) -> list[int]:
        pass

    def key(self):
        pass


@dataclass
class CombinerProperty:
    A: str
    B: str
    C: str
    D: str
    A_alpha: str
    B_alpha: str
    C_alpha: str
    D_alpha: str

    def key(self) -> tuple[str, str, str, str, str, str, str, str]:
        pass


@dataclass
class ProceduralAnimProperty:
    speed: float
    amplitude: float
    frequency: float
    spaceFrequency: float
    offset: float
    noiseAmplitude: float
    animate: bool
    animType: str

    def key(self):
        pass


@dataclass
class ProcAnimVectorProperty:
    x: ProceduralAnimProperty
    y: ProceduralAnimProperty
    z: ProceduralAnimProperty
    pivot: list[float]
    angularSpeed: float
    menu: bool

    def key(self):
        pass


@dataclass
class PrimDepthSettings:
    z: int
    dz: int

    def key(self):
        pass


@dataclass
class RDPSettings:
    g_zbuffer: bool
    g_shade: bool
    # v1/2 difference
    g_cull_front: bool
    # v1/2 difference
    g_cull_back: bool
    g_fog: bool
    g_lighting: bool
    g_tex_gen: bool
    g_tex_gen_linear: bool
    # v1/2 difference
    g_shade_smooth: bool
    # f3dlx2 only
    g_clipping: bool
    # upper half mode
    # v2 only
    g_mdsft_alpha_dither: str
    # v2 only
    g_mdsft_rgb_dither: str
    g_mdsft_combkey: str
    g_mdsft_textconv: str
    g_mdsft_text_filt: str
    g_mdsft_textlut: str
    g_mdsft_textlod: str
    num_textures_mipmapped: int
    g_mdsft_textdetail: str
    g_mdsft_textpersp: str
    g_mdsft_cycletype: str
    # v1 only
    g_mdsft_color_dither: str
    g_mdsft_pipeline: str
    # lower half mode
    g_mdsft_alpha_compare: str
    g_mdsft_zsrcsel: str
    prim_depth: PrimDepthSettings
    clip_ratio: int

    # cycle independent
    set_rendermode: bool
    rendermode_advanced_enabled: bool
    rendermode_preset_cycle_1: str
    rendermode_preset_cycle_2: str
    aa_en: bool
    z_cmp: bool
    z_upd: bool
    im_rd: bool
    clr_on_cvg: bool
    cvg_dst: str
    zmode: str
    cvg_x_alpha: bool
    alpha_cvg_sel: bool
    force_bl: bool

    # cycle dependent - (P * A + M - B) / (A + B)
    blend_p1: str
    blend_p2: str
    blend_m1: str
    blend_m2: str
    blend_a1: str
    blend_a2: str
    blend_b1: str
    blend_b2: str

    def key(self):
        pass


@dataclass
class F3DMaterialProperty:
    presetName: str

    scale_autoprop: bool
    uv_basis: str

    # Combiners
    combiner1: CombinerProperty
    combiner2: CombinerProperty

    # Texture animation
    menu_procAnim: bool
    UVanim0: ProcAnimVectorProperty
    UVanim1: ProcAnimVectorProperty

    # material textures
    tex_scale: list[float]
    tex0: TextureProperty
    tex1: TextureProperty

    # Should Set?

    set_prim: bool
    set_lights: bool
    set_env: bool
    set_blend: bool
    set_key: bool
    set_k0_5: bool
    set_combiner: bool
    use_default_lighting: bool

    # Blend Color
    blend_color: list[float]
    prim_color: list[float]
    env_color: list[float]
    key_center: list[float]

    # Chroma
    key_scale: list[float]
    key_width: list[float]

    # Convert
    k0: float
    k1: float
    k2: float
    k3: float
    k4: float
    k5: float

    # Prim
    prim_lod_frac: float
    prim_lod_min: float

    # lights
    default_light_color: list[float]
    set_ambient_from_light: bool
    ambient_light_color: list[float]
    f3d_light1: "Light"
    f3d_light2: "Light"
    f3d_light3: "Light"
    f3d_light4: "Light"
    f3d_light5: "Light"
    f3d_light6: "Light"
    f3d_light7: "Light"

    # Fog Properties
    fog_color: list[float]
    # TODO: (V5) dragorn421 should ask me if this is _actually_ the fog position max because this seems wrong to him
    fog_position: list[int]
    set_fog: bool
    use_global_fog: bool

    # geometry mode
    menu_geo: bool
    menu_upper: bool
    menu_lower: bool
    menu_other: bool
    menu_lower_render: bool
    rdp_settings: RDPSettings

    draw_layer: DrawLayerProperty
    use_large_textures: bool
    large_edges: str

    def key(self):
        pass


# parser props


@dataclass
class ImportFileProperty:
    path: str


# flipbook props


@dataclass
class FlipbookImagePointerProperty:
    image: "Image"
    name: str


@dataclass
class FlipbookProperty:
    enable: bool
    name: str
    exportMode: str
    textures: Collection[FlipbookImagePointerProperty]


@dataclass
class FlipbookGroupProperty:
    flipbook0: FlipbookProperty
    flipbook1: FlipbookProperty


# op largetexture props


@dataclass
class OpLargeTextureProperty:
    mat: "Material"
    clamp_border: float
    total_size_s: int
    total_size_t: int
    lose_pixels: bool
    bias: str
    scale: float


# lib


@dataclass
class F3D_WorldLib:
    rdp_defaults: RDPSettings
    menu_geo: bool
    menu_upper: bool
    menu_lower: bool
    menu_other: bool
    menu_layers: bool


@dataclass
class F3D_MaterialLib:
    is_f3d: bool
    mat_ver: int
    f3d_update_flag: bool
    f3d_mat: F3DMaterialProperty
    menu_tab: str
    flipbookGroup: FlipbookGroupProperty


@dataclass
class F3D_SceneLib:
    f3d_type: str
    isHWv1: bool
    f3dUserPresetsOnly: bool
    f3d_simple: bool
    DLImportName: str
    DLImportPath: str
    DLImportBasePath: str
    DLRemoveDoubles: bool
    DLImportNormals: bool
    DLImportDrawLayer: str
    DLImportOtherFiles: Collection[ImportFileProperty]
    DLImportOtherFilesIndex: int
    matWriteMethod: str
    opLargeTextureProperty: OpLargeTextureProperty


@dataclass
class F3D_ObjectLib:
    use_f3d_culling: bool
    ignore_render: bool
    ignore_collision: bool
    f3d_lod_z: int
    f3d_lod_always_render_farthest: bool
