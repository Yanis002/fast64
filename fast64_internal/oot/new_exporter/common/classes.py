from dataclasses import dataclass, field
from math import radians
from mathutils import Quaternion, Matrix
from bpy.types import Object
from ....utility import PluginError, indent
from ...oot_utility import ootConvertTranslation, ootConvertRotation
from ...actor.properties import OOTActorHeaderProperty


altHeaderList = ["childNight", "adultDay", "adultNight"]


@dataclass
class Common:
    """This class hosts common data used across different sub-systems of this exporter"""

    sceneObj: Object
    transform: Matrix
    roomIndex: int = None

    def getRoomObjectFromChild(self, childObj: Object) -> Object | None:
        """Returns the room empty object from one of its child"""

        # Note: temporary solution until PRs #243 & #255 are merged
        for obj in self.sceneObj.children_recursive:
            if obj.type == "EMPTY" and obj.ootEmptyType == "Room":
                for o in obj.children_recursive:
                    if o == childObj:
                        return obj
        return None

    def validateCurveData(self, curveObj: Object):
        """Performs safety checks related to curve objects"""

        curveData = curveObj.data
        if curveObj.type != "CURVE" or curveData.splines[0].type != "NURBS":
            # Curve was likely not intended to be exported
            return False

        if len(curveData.splines) != 1:
            # Curve was intended to be exported but has multiple disconnected segments
            raise PluginError(f"Exported curves should have only one single segment, found {len(curveData.splines)}")

        return True

    def roundPosition(self, position) -> tuple[int, int, int]:
        """Returns the rounded position values"""

        return (round(position[0]), round(position[1]), round(position[2]))

    def isCurrentHeaderValid(self, headerSettings: OOTActorHeaderProperty, headerIndex: int):
        """Checks if the an alternate header can be used"""

        preset = headerSettings.sceneSetupPreset

        if preset == "All Scene Setups" or (preset == "All Non-Cutscene Scene Setups" and headerIndex < 4):
            return True

        if preset == "Custom":
            for i, header in enumerate(["childDay"] + altHeaderList):
                if getattr(headerSettings, f"{header}Header") and i == headerIndex:
                    return True

            for csHeader in headerSettings.cutsceneHeaders:
                if csHeader.headerIndex == headerIndex:
                    return True

        return False

    def getPropValue(self, data, propName: str):
        """Returns a property's value based on if the value is 'Custom'"""

        value = getattr(data, propName)
        return value if value != "Custom" else getattr(data, f"{propName}Custom")

    def getConvertedTransformWithOrientation(
        self, transform: Matrix, sceneObj: Object, obj: Object, orientation: Quaternion | Matrix
    ):
        relativeTransform = transform @ sceneObj.matrix_world.inverted() @ obj.matrix_world
        blenderTranslation, blenderRotation, scale = relativeTransform.decompose()
        rotation = blenderRotation @ orientation
        convertedTranslation = ootConvertTranslation(blenderTranslation)
        convertedRotation = ootConvertRotation(rotation)

        return convertedTranslation, convertedRotation, scale, rotation

    def getConvertedTransform(self, transform: Matrix, sceneObj: Object, obj: Object, handleOrientation: bool):
        # Hacky solution to handle Z-up to Y-up conversion
        # We cannot apply rotation to empty, as that modifies scale
        if handleOrientation:
            orientation = Quaternion((1, 0, 0), radians(90.0))
        else:
            orientation = Matrix.Identity(4)
        return self.getConvertedTransformWithOrientation(transform, sceneObj, obj, orientation)

    def getAltHeaderListCmd(self, altName: str):
        """Returns the scene alternate header list command"""

        return indent + f"SCENE_CMD_ALTERNATE_HEADER_LIST({altName}),\n"

    def getEndCmd(self):
        """Returns the scene end command"""

        return indent + "SCENE_CMD_END(),\n"


@dataclass
class Actor:
    """Defines an Actor"""

    name: str = None
    id: str = None
    pos: list[int] = field(default_factory=list)
    rot: str = None
    params: str = None

    def getActorEntry(self):
        """Returns a single actor entry"""

        posData = "{ " + ", ".join(f"{round(p)}" for p in self.pos) + " }"
        rotData = "{ " + self.rot + " }"

        actorInfos = [self.id, posData, rotData, self.params]
        infoDescs = ["Actor ID", "Position", "Rotation", "Parameters"]

        return (
            indent
            + (f"// {self.name}\n" + indent if self.name != "" else "")
            + "{\n"
            + ",\n".join((indent * 2) + f"/* {desc:10} */ {info}" for desc, info in zip(infoDescs, actorInfos))
            + ("\n" + indent + "},\n")
        )


@dataclass
class TransitionActor(Actor):
    """Defines a Transition Actor"""

    dontTransition: bool = None
    roomFrom: int = None
    roomTo: int = None
    cameraFront: str = None
    cameraBack: str = None

    def getTransitionActorEntry(self):
        """Returns a single transition actor entry"""

        sides = [(self.roomFrom, self.cameraFront), (self.roomTo, self.cameraBack)]
        roomData = "{ " + ", ".join(f"{room}, {cam}" for room, cam in sides) + " }"
        posData = "{ " + ", ".join(f"{round(pos)}" for pos in self.pos) + " }"

        actorInfos = [roomData, self.id, posData, self.rot, self.params]
        infoDescs = ["Room & Cam Index (Front, Back)", "Actor ID", "Position", "Rotation Y", "Parameters"]

        return (
            (indent + f"// {self.name}\n" + indent if self.name != "" else "")
            + "{\n"
            + ",\n".join((indent * 2) + f"/* {desc:30} */ {info}" for desc, info in zip(infoDescs, actorInfos))
            + ("\n" + indent + "},\n")
        )


@dataclass
class EntranceActor(Actor):
    """Defines an Entrance Actor"""

    roomIndex: int = None
    spawnIndex: int = None

    def getSpawnEntry(self):
        """Returns a single spawn entry"""

        return indent + "{ " + f"{self.spawnIndex}, {self.roomIndex}" + " },\n"
