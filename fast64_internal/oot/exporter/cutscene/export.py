from bpy.types import Object
from ...scene.classes import OOTSceneHeaderProperty
from ...cutscene.classes import OOTCutsceneProperty
from ..utility import getCustomProperty
from ..classes.scene import OOTScene

from ..classes.cutscene import (
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


def getCutsceneName(obj):
    name = obj.name
    if name.startswith("Cutscene."):
        name = name[9:]
    name = name.replace(".", "_")
    return name


def convertCutsceneData(csParentOut: OOTScene | OOTCutscene, csParentIn: OOTSceneHeaderProperty | OOTCutsceneProperty):
    for listIn in csParentIn.csLists:
        listOut = OOTCSList()
        listOut.listType = listIn.listType
        listOut.unkType, listOut.fxType, listOut.fxStartFrame, listOut.fxEndFrame = (
            listIn.unkType,
            listIn.fxType,
            listIn.fxStartFrame,
            listIn.fxEndFrame,
        )

        if listOut.listType == "Textbox":
            for entryIn in listIn.textbox:
                entryOut = OOTCSTextbox()
                entryOut.textboxType = entryIn.textboxType
                entryOut.messageId = entryIn.messageId
                entryOut.ocarinaSongAction = entryIn.ocarinaSongAction
                entryOut.startFrame = entryIn.startFrame
                entryOut.endFrame = entryIn.endFrame
                entryOut.type = entryIn.type
                entryOut.topOptionBranch = entryIn.topOptionBranch
                entryOut.bottomOptionBranch = entryIn.bottomOptionBranch
                entryOut.ocarinaMessageId = entryIn.ocarinaMessageId
                listOut.entries.append(entryOut)
        elif listOut.listType == "Lighting":
            for entryIn in listIn.lighting:
                entryOut = OOTCSLighting()
                entryOut.index = entryIn.index
                entryOut.startFrame = entryIn.startFrame
                listOut.entries.append(entryOut)
        elif listOut.listType == "Time":
            for entryIn in listIn.time:
                entryOut = OOTCSTime()
                entryOut.startFrame = entryIn.startFrame
                entryOut.hour = entryIn.hour
                entryOut.minute = entryIn.minute
                listOut.entries.append(entryOut)
        elif listOut.listType in {"PlayBGM", "StopBGM", "FadeBGM"}:
            for entryIn in listIn.bgm:
                entryOut = OOTCSBGM()
                entryOut.value = entryIn.value
                entryOut.startFrame = entryIn.startFrame
                entryOut.endFrame = entryIn.endFrame
                listOut.entries.append(entryOut)
        elif listOut.listType == "Misc":
            for entryIn in listIn.misc:
                entryOut = OOTCSMisc()
                entryOut.operation = entryIn.operation
                entryOut.startFrame = entryIn.startFrame
                entryOut.endFrame = entryIn.endFrame
                listOut.entries.append(entryOut)
        elif listOut.listType == "0x09":
            for entryIn in listIn.nine:
                entryOut = OOTCS0x09()
                entryOut.startFrame = entryIn.startFrame
                entryOut.unk2 = entryIn.unk2
                entryOut.unk3 = entryIn.unk3
                entryOut.unk4 = entryIn.unk4
                listOut.entries.append(entryOut)
        elif listOut.listType == "Unk":
            for entryIn in listIn.unk:
                entryOut = OOTCSUnk()
                entryOut.unk1 = entryIn.unk1
                entryOut.unk2 = entryIn.unk2
                entryOut.unk3 = entryIn.unk3
                entryOut.unk4 = entryIn.unk4
                entryOut.unk5 = entryIn.unk5
                entryOut.unk6 = entryIn.unk6
                entryOut.unk7 = entryIn.unk7
                entryOut.unk8 = entryIn.unk8
                entryOut.unk9 = entryIn.unk9
                entryOut.unk10 = entryIn.unk10
                entryOut.unk11 = entryIn.unk11
                entryOut.unk12 = entryIn.unk12
                listOut.entries.append(entryOut)
        csParentOut.csLists.append(listOut)


def processCutscene(inCSObj: Object):
    outCs = OOTCutscene()
    outCs.name = getCutsceneName(inCSObj)
    csProp = inCSObj.ootCutsceneProperty
    outCs.csEndFrame = getCustomProperty(csProp, "csEndFrame")
    outCs.csWriteTerminator = getCustomProperty(csProp, "csWriteTerminator")
    outCs.csTermIdx = getCustomProperty(csProp, "csTermIdx")
    outCs.csTermStart = getCustomProperty(csProp, "csTermStart")
    outCs.csTermEnd = getCustomProperty(csProp, "csTermEnd")
    convertCutsceneData(outCs, csProp)
    return outCs
