from ....utility import CData
from .export import ExportInfo, CullGroup, OOTObjectCategorizer, BoxEmpty
from .scene import OOTScene, OOTExit, OOTLight, OOTPath
from .room import OOTDLGroup, OOTRoomMesh, OOTRoom, OOTRoomMeshGroup
from .animation import OOTAnimation
from .actor import OOTActor, OOTTransitionActor, OOTEntrance
from .skeleton import OOTSkeleton, OOTLimb

from .cutscene import (
    OOTCSList,
    OOTCSTextbox,
    OOTCSLighting,
    OOTCSTime,
    OOTCSBGM,
    OOTCSMisc,
    OOTCS0x09,
    OOTCSUnk,
    OOTCutscene,
)

from .collision import (
    OOTCollision,
    OOTCollisionVertex,
    OOTCollisionPolygon,
    OOTPolygonType,
    OOTCameraData,
    OOTCameraPosData,
    OOTWaterBox,
)


class OOTSceneC:
    def __init__(self):
        # Main header file for both the scene and room(s)
        self.header = CData()

        # Files for the scene segment
        self.sceneMainC = CData()
        self.sceneTexturesC = CData()
        self.sceneCollisionC = CData()
        self.sceneCutscenesC: list[CData] = []

        # Files for room segments
        self.roomMainC: dict[str, CData] = {}
        self.roomMeshInfoC: dict[str, CData] = {}
        self.roomMeshC: dict[str, CData] = {}

    def sceneTexturesIsUsed(self):
        return len(self.sceneTexturesC.source) > 0

    def sceneCutscenesIsUsed(self):
        return len(self.sceneCutscenesC) > 0


class OOTCommonCommands:
    def getAltLayersListCmd(self, altLayerListName: str):
        """Returns the alternate scene layer command"""
        return f"SCENE_CMD_ALTERNATE_HEADER_LIST({altLayerListName})"

    def getEndMarkerCmd(self):
        """Returns the end marker command, common to scenes and rooms"""
        # ``SCENE_CMD_END`` defines the end of scene commands
        return "SCENE_CMD_END(),\n"
