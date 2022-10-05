class OOTActor:
    def __init__(self, actorID: str, position: list[int], rotation: list[str], actorParam: str):
        self.actorID = actorID
        self.actorParam = actorParam
        self.position = position
        self.rotation = rotation


class OOTTransitionActor:
    def __init__(
        self, actorID: str,
        frontRoom: int,
        backRoom: int,
        frontCam: str,
        backCam: str,
        position: list[int],
        rotationY: int,
        actorParam: str
):
        self.actorID = actorID
        self.actorParam = actorParam
        self.frontRoom = frontRoom
        self.backRoom = backRoom
        self.frontCam = frontCam
        self.backCam = backCam
        self.position = position
        self.rotationY = rotationY


class OOTEntrance:
    def __init__(self, roomIndex: int, startPositionIndex: int):
        self.roomIndex = roomIndex
        self.startPositionIndex = startPositionIndex
