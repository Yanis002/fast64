from .....utility import CData, PluginError
from ...data import indent
from ...classes.scene import OOTScene
from ...classes.cutscene import OOTCutscene
from .data import ootEnumCSListTypeListC, ootEnumCSListTypeEntryC, ootEnumCSTextboxTypeEntryC


def getCutsceneIncludes(fileName: str):
    includeData = CData()

    includeFiles = [
        "ultra64.h",
        "z64.h",
        "macros.h",
        "command_macros_base.h",
        "z64cutscene_commands.h",
        f"{fileName}",
    ]

    includeData.source = "\n".join([f'#include "{include}"' for include in includeFiles]) + "\n\n"
    return includeData


def getCutsceneArray(csParent: OOTCutscene | OOTScene, csName: str):
    csData = CData()
    csDataName = f"CutsceneData {csName}[]"

    # .h
    csData.header = f"extern {csDataName};\n"

    # .c
    csData.source = csDataName + " = {\n"

    lenEntries = len(csParent.csLists)
    if csParent.csWriteTerminator:
        lenEntries += 1

    csData.source += indent + f"CS_BEGIN_CUTSCENE({lenEntries}, {csParent.csEndFrame}),\n"

    if csParent.csWriteTerminator:
        csData.source += (
            indent + f"CS_TERMINATOR({csParent.csTermIdx}, {csParent.csTermStart}, {csParent.csTermEnd}),\n"
        )

    for list in csParent.csLists:
        csData.source += indent + ootEnumCSListTypeListC[list.listType] + "("

        if list.listType == "Unk":
            csData.source += f"{list.unkType}, "

        if list.listType == "FX":
            csData.source += f"{list.fxType}, {list.fxStartFrame}, {list.fxEndFrame}"
        else:
            csData.source += str(len(list.entries))

        csData.source += "),\n"

        for e in list.entries:
            csData.source += indent * 2

            if list.listType == "Textbox":
                csData.source += ootEnumCSTextboxTypeEntryC[e.textboxType]
            else:
                csData.source += ootEnumCSListTypeEntryC[list.listType]

            csData.source += "("

            match list.listType:
                case "Textbox":
                    if e.textboxType == "Text":
                        csData.source += (
                            f"{e.messageId}, {e.startFrame}, {e.endFrame}, "
                            + f"{e.type}, {e.topOptionBranch}, {e.bottomOptionBranch}"
                        )
                    elif e.textboxType == "None":
                        csData.source += f"{e.startFrame}, {e.endFrame}"
                    elif e.textboxType == "LearnSong":
                        csData.source += f"{e.ocarinaSongAction}, {e.startFrame}, {e.endFrame}, {e.ocarinaMessageId}"
                case "Lighting":
                    csData.source += f"{e.index}, {e.startFrame}, {e.startFrame + 1}{', 0' * 8}"
                case "Time":
                    csData.source += f"1, {e.startFrame}, {e.startFrame + 1}, {e.hour}, {e.minute}, 0"
                case "PlayBGM" | "StopBGM" | "FadeBGM":
                    csData.source += e.value

                    if list.listType != "FadeBGM":
                        csData.source += " + 1"  # Game subtracts 1 to get actual seq

                    csData.source += f", {e.startFrame}, {e.endFrame}{', 0' * 8}"
                case "Misc":
                    csData.source += f"{e.operation}, {e.startFrame}, {e.endFrame}{', 0' * 11}"
                case "0x09":
                    csData.source += f"0, {e.startFrame}, {e.startFrame + 1}, {e.unk2}, {e.unk3}, {e.unk4}, 0, 0"
                case "Unk":
                    csData.source += (
                        f"{e.unk1}, {e.unk2}, {e.unk3}, {e.unk4}, {e.unk5}, {e.unk6}, "
                        + f"{e.unk7}, {e.unk8}, {e.unk9}, {e.unk10}, {e.unk11}, {e.unk12}"
                    )
                case _:
                    raise PluginError("Internal error: invalid cutscene list type " + list.listType)

            csData.source += "),\n"

    csData.source += indent + "CS_END(),\n};\n\n"
    return csData


def convertCutsceneToC(outScene: OOTScene):
    """Returns the cutscene data"""
    csData: list[CData] = []
    sceneLayers: list[OOTScene] = [
        outScene,
        outScene.childNightHeader,
        outScene.adultDayHeader,
        outScene.adultNightHeader,
    ]
    sceneLayers.extend(outScene.cutsceneHeaders)

    for i, layer in enumerate(sceneLayers):
        if layer is not None and layer.writeCutscene:
            data = CData()
            if layer.csWriteType == "Embedded":
                data = getCutsceneArray(layer, layer.getCutsceneDataName(i))
            elif layer.csWriteType == "Object":
                data = getCutsceneArray(layer.csWriteObject, layer.csWriteObject.name)
            csData.append(data)

    for extraCs in outScene.extraCutscenes:
        csData.append(getCutsceneArray(extraCs, extraCs.name))

    return csData
