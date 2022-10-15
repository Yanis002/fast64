import bpy
from bpy.types import Object
from math import radians
from re import search, escape, finditer, DOTALL
from ....utility import PluginError, readFile, hexOrDecInt

from ...utility import (
    getStartBone,
    getSortedChildren,
)


def getNextBone(boneStack, armatureObj: Object):
    if len(boneStack) == 0:
        raise PluginError("More bones in animation than on armature.")

    bone = armatureObj.data.bones[boneStack[0]]
    boneStack = boneStack[1:]
    boneStack = getSortedChildren(armatureObj, bone) + boneStack

    return bone, boneStack


def getFrameData(filepath: str, animData: str, frameDataName: str):
    matchResult = search(escape(frameDataName) + "\s*\[\s*[0-9]*\s*\]\s*=\s*\{([^\}]*)\}", animData, DOTALL)

    if matchResult is None:
        raise PluginError(f"Cannot find animation frame data named '{frameDataName}' in '{filepath}'")

    return [
        int.from_bytes([int(value.strip()[2:4], 16), int(value.strip()[4:6], 16)], "big", signed=True)
        for value in matchResult.group(1).split(",")
        if value.strip() != ""
    ]


def getJointIndices(filepath: str, animData: str, jointIndicesName: str):
    matchResult = search(escape(jointIndicesName) + "\s*\[\s*[0-9]*\s*\]\s*=\s*\{([^;]*);", animData, DOTALL)

    if matchResult is None:
        raise PluginError(f"Cannot find animation joint indices data named '{jointIndicesName}' in '{filepath}'")

    return [
        [hexOrDecInt(match.group(i)) for i in range(1, 4)]
        for match in finditer("\{([^,\}]*),([^,\}]*),([^,\}]*)\s*,?\s*\}", matchResult.group(1), DOTALL)
    ]


def ootImportAnimationC(armatureObj: Object, filepath: str, animName: str, actorScale: int):
    animData = readFile(filepath)

    matchResult = search(
        escape(animName) + "\s*=\s*\{\s*\{\s*([^,\s]*)\s*\}*\s*,\s*([^,\s]*)\s*,\s*([^,\s]*)\s*,\s*([^,\s]*)\s*\}\s*;",
        animData,
    )

    if matchResult is None:
        raise PluginError("Cannot find animation named " + animName + " in " + filepath)

    frameCount = hexOrDecInt(matchResult.group(1).strip())
    frameDataName = matchResult.group(2).strip()
    jointIndicesName = matchResult.group(3).strip()
    staticIndexMax = hexOrDecInt(matchResult.group(4).strip())

    frameData = getFrameData(filepath, animData, frameDataName)
    jointIndices = getJointIndices(filepath, animData, jointIndicesName)

    bpy.context.scene.frame_end = frameCount
    anim = bpy.data.actions.new(animName)

    startBoneName = getStartBone(armatureObj)
    boneStack = [startBoneName]

    isRootTranslation = True
    # boneFrameData = [[x keyframes], [y keyframes], [z keyframes]]
    # len(armatureFrameData) should be = number of bones
    # property index = 0,1,2 (aka x,y,z)
    for jointIndex in jointIndices:
        if isRootTranslation:
            for propertyIndex in range(3):
                fcurve = anim.fcurves.new(
                    data_path='pose.bones["' + startBoneName + '"].location',
                    index=propertyIndex,
                    action_group=startBoneName,
                )

                if jointIndex[propertyIndex] < staticIndexMax:
                    value = frameData[jointIndex[propertyIndex]] / actorScale
                    fcurve.keyframe_points.insert(0, value)
                else:
                    for frame in range(frameCount):
                        value = frameData[jointIndex[propertyIndex] + frame] / actorScale
                        fcurve.keyframe_points.insert(frame, value)

            isRootTranslation = False
        else:
            # WARNING: This assumes the order bones are processed are in alphabetical order.
            # If this changes in the future, then this won't work.
            bone, boneStack = getNextBone(boneStack, armatureObj)

            for propertyIndex in range(3):
                fcurve = anim.fcurves.new(
                    data_path='pose.bones["' + bone.name + '"].rotation_euler',
                    index=propertyIndex,
                    action_group=bone.name,
                )

                if jointIndex[propertyIndex] < staticIndexMax:
                    value = radians(frameData[jointIndex[propertyIndex]] * 360 / (2**16))
                    fcurve.keyframe_points.insert(0, value)
                else:
                    for frame in range(frameCount):
                        value = radians(frameData[jointIndex[propertyIndex] + frame] * 360 / (2**16))
                        fcurve.keyframe_points.insert(frame, value)

    if armatureObj.animation_data is None:
        armatureObj.animation_data_create()

    armatureObj.animation_data.action = anim
