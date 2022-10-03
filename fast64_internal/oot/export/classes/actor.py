class OOTActor:
    def __init__(self, actorID, position, rotation, actorParam, rotOverride):
        self.actorID = actorID
        self.actorParam = actorParam
        self.rotOverride = rotOverride
        self.position = position
        self.rotation = rotation


class OOTTransitionActor:
    def __init__(self, actorID, frontRoom, backRoom, frontCam, backCam, position, rotationY, actorParam):
        self.actorID = actorID
        self.actorParam = actorParam
        self.frontRoom = frontRoom
        self.backRoom = backRoom
        self.frontCam = frontCam
        self.backCam = backCam
        self.position = position
        self.rotationY = rotationY


class OOTEntrance:
    def __init__(self, roomIndex, startPositionIndex):
        self.roomIndex = roomIndex
        self.startPositionIndex = startPositionIndex
