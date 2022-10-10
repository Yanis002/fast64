from ....utility import CData, toAlnum
from ...oot_utility import indent


class OOTAnimation:
    def __init__(self, name: str):
        self.name = toAlnum(name)
        self.segmentID = None
        self.indices = {}
        self.values = []
        self.frameCount = None
        self.limit = None

    def valuesName(self):
        return f"{self.name}FrameData"

    def indicesName(self):
        return f"{self.name}JointIndices"

    def toC(self):
        animData = CData()
        animData.source += '#include "ultra64.h"\n#include "global.h"\n\n'

        # values
        animData.source += f"s16 {self.valuesName()}[{len(self.values)}]" + " = {\n" + indent

        counter = 0
        for value in self.values:
            animData.source += f"0x{value:04X}, "
            counter += 1

            if counter >= 16:  # round number for finding/counting data
                animData.source += "\n" + indent
                counter = 0

        animData.source += "\n};\n\n"

        # indices (index -1 => translation)
        # index for frame data array
        animData.source += f"JointIndex {self.indicesName()}[{len(self.indices)}]" + " = {\n"
        for index in range(-1, len(self.indices) - 1):
            animData.source += (
                indent + "{ " + ", ".join([f"{self.indices[index][field]}" for field in range(3)]) + " },\n"
            )
        animData.source += "};\n\n"

        # animation header
        animName = f"AnimationHeader {self.name}"
        animData.header += f"extern {animName};\n"
        animData.source += (
            animName
            + " = {\n"
            + indent
            + f"{self.frameCount}, {self.valuesName()}, {self.indicesName()}, {self.limit}\n"
            + "};\n\n"
        )

        return animData
