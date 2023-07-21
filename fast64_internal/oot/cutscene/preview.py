import bpy

from bpy.types import Scene, Object
from bpy.app.handlers import persistent
from ...utility import gammaInverse, hexOrDecInt


def getLerp(max: float, min: float, val: float):
    # from ``Environment_LerpWeight()``
    diff = max - min
    ret = None

    if diff != 0.0:
        ret = 1.0 - (max - val) / diff

        if not ret >= 1.0:
            return ret

    return 1.0


def getColor(value: float) -> float:
    return gammaInverse([value / 0xFF, 0.0, 0.0])[0]


def setupCompositorNodes():
    if bpy.app.version < (3, 6, 0):
        return False

    if not bpy.context.scene.use_nodes:
        bpy.context.scene.use_nodes = True
        bpy.context.scene.ootCSPreviewNodesReady = False

    space = None
    for area in bpy.context.screen.areas:
        if (area != bpy.context.area) and (area.type == 'VIEW_3D'):
            for space in area.spaces:
                if space.type == "VIEW_3D":
                    break
    if space is not None and space.shading.use_compositor != "CAMERA":
        space.shading.use_compositor = "CAMERA"

    if bpy.context.scene.ootCSPreviewNodesReady:
        return True

    nodeTree = bpy.context.scene.node_tree
    nodeRenderLayer = nodeComposite = nodeMixRGB = nodeRGBTrans = nodeAlphaTrans = nodeRGBMisc = nodeMixRGBMisc = None
    for node in nodeTree.nodes.values():
        if node.type == "R_LAYERS":
            nodeRenderLayer = node
        if node.type == "COMPOSITE":
            nodeComposite = node
        if node.label == "CSPreview_MixRGB":
            nodeMixRGB = node
        if node.label == "CSTrans_RGB":
            nodeRGBTrans = node
        if node.label == "CSMisc_RGB":
            nodeRGBMisc = node
        if node.label == "CSTrans_AlphaOver":
            nodeAlphaTrans = node
        if node.label == "CSMisc_MixRGB":
            nodeMixRGBMisc = node

    if nodeRenderLayer is None:
        nodeRenderLayer = nodeTree.nodes.new("CompositorNodeRLayers")
    nodeRenderLayer.select = False
    nodeRenderLayer.name = nodeRenderLayer.label = "CSPreview_RenderLayer"
    nodeRenderLayer.location = (-500, 0)

    if nodeRGBTrans is None:
        nodeRGBTrans = nodeTree.nodes.new("CompositorNodeRGB")
    nodeRGBTrans.select = False
    nodeRGBTrans.name = nodeRGBTrans.label = "CSTrans_RGB"
    nodeRGBTrans.location = (-200, 0)
    bpy.context.scene.node_tree.nodes["CSTrans_RGB"].outputs[0].default_value = [0.0, 0.0, 0.0, 0.0]

    if nodeRGBMisc is None:
        nodeRGBMisc = nodeTree.nodes.new("CompositorNodeRGB")
    nodeRGBMisc.select = False
    nodeRGBMisc.name = nodeRGBMisc.label = "CSMisc_RGB"
    nodeRGBMisc.location = (-200, -200)
    bpy.context.scene.node_tree.nodes["CSMisc_RGB"].outputs[0].default_value = [0.0, 0.0, 0.0, 0.0]

    if nodeAlphaTrans is None:
        nodeAlphaTrans = nodeTree.nodes.new("CompositorNodeAlphaOver")
    nodeAlphaTrans.select = False
    nodeAlphaTrans.name = nodeAlphaTrans.label = "CSTrans_AlphaOver"
    nodeAlphaTrans.location = (0, 0)

    if nodeMixRGBMisc is None:
        nodeMixRGBMisc = nodeTree.nodes.new("CompositorNodeMixRGB")
    nodeMixRGBMisc.select = False
    nodeMixRGBMisc.name = nodeMixRGBMisc.label = "CSMisc_MixRGB"
    nodeMixRGBMisc.location = (0, -200)
    nodeMixRGBMisc.use_alpha = True
    nodeMixRGBMisc.blend_type = "COLOR"

    if nodeMixRGB is None:
        nodeMixRGB = nodeTree.nodes.new("CompositorNodeMixRGB")
    nodeMixRGB.select = False
    nodeMixRGB.name = nodeMixRGB.label = "CSPreview_MixRGB"
    nodeMixRGB.location = (200, 0)
    nodeMixRGB.blend_type = "COLOR"

    if nodeComposite is None:
        nodeComposite = nodeTree.nodes.new("CompositorNodeComposite")
    nodeComposite.select = True
    nodeComposite.name = nodeComposite.label = "CSPreview_Composite"
    nodeComposite.location = (400, 0)

    nodeTree.links.new(nodeAlphaTrans.inputs[1], nodeRenderLayer.outputs[0])
    nodeTree.links.new(nodeMixRGBMisc.inputs[1], nodeRenderLayer.outputs[0])
    nodeTree.links.new(nodeAlphaTrans.inputs[2], nodeRGBTrans.outputs[0])
    nodeTree.links.new(nodeMixRGBMisc.inputs[2], nodeRGBMisc.outputs[0])
    nodeTree.links.new(nodeMixRGB.inputs[1], nodeAlphaTrans.outputs[0])
    nodeTree.links.new(nodeMixRGB.inputs[2], nodeMixRGBMisc.outputs[0])
    nodeTree.links.new(nodeComposite.inputs[0], nodeMixRGB.outputs[0])

    bpy.context.scene.ootCSPreviewNodesReady = True
    return True


@persistent
def cutscenePreviewFrameHandler(scene: Scene):
    csObj: Object = bpy.context.scene.ootCSPreviewCSObj

    if csObj is None or not csObj.type == "EMPTY" and not csObj.ootEmptyType == "Cutscene":
        print("ERROR: Current Object is not a cutscene!")
        return

    useNodeFeatures = setupCompositorNodes()
    
    cameraObjects = [None, None]
    for obj in csObj.children:
        if obj.type == "CAMERA":
            cameraObjects[1] = obj
            break
        
    foundObj = None
    for obj in bpy.data.objects:
        if obj.type == "CAMERA" and obj.parent is not None and obj.parent.ootEmptyType in ["Scene", "Room"]:
            camPosProp = obj.ootCameraPositionProperty
            camTypes = ["CAM_SET_PREREND0", "CAM_SET_PREREND_FIXED"]
            if camPosProp.camSType != "Custom" and camPosProp.camSType in camTypes:
                foundObj = obj
                break
            elif camPosProp.camSType == "Custom":
                if camPosProp.camSTypeCustom.startswith("0x"):
                    if hexOrDecInt(camPosProp.camSTypeCustom) == 25:
                        foundObj = obj
                        break
                elif camPosProp.camSTypeCustom in camTypes:
                    foundObj = obj
                    break

    if foundObj is not None:
        cameraObjects[0] = foundObj

    # Simulate cutscene for all frames up to present
    for curFrame in range(bpy.context.scene.frame_current):
        if curFrame == 0:
            if useNodeFeatures:
                color = [0.0, 0.0, 0.0, 0.0]

                bpy.context.scene.node_tree.nodes["CSTrans_RGB"].outputs[0].default_value = color
                bpy.context.scene.node_tree.nodes["CSMisc_RGB"].outputs[0].default_value = color
            csObj.ootCutsceneProperty.preview.isFixedCamSet = False
            bpy.context.scene.camera = cameraObjects[1]
            curFrame += 1

        if useNodeFeatures:
            for transitionCmd in csObj.ootCutsceneProperty.preview.transitionList:
                startFrame = transitionCmd.startFrame
                endFrame = transitionCmd.endFrame

                if curFrame >= startFrame and curFrame <= endFrame:
                    color = [0.0, 0.0, 0.0, 0.0]
                    lerp = getLerp(endFrame, startFrame, curFrame)
                    linear255 = getColor(255.0)
                    linear160 = getColor(160.0)
                    linear155 = getColor(155.0)

                    if transitionCmd.type.endswith("IN"):
                        alpha = linear255 * lerp
                    else:
                        alpha = (1.0 - lerp) * linear255

                    if "HALF" in transitionCmd.type:
                        if "_IN_" in transitionCmd.type:
                            alpha = linear255 - ((1.0 - lerp) * linear155)
                        else:
                            alpha = linear255 - (linear155 * lerp)

                    if "_GRAY_" in transitionCmd.type:
                        color[0] = color[1] = color[2] = linear160 * alpha
                    elif "_RED_" in transitionCmd.type:
                        color[0] = linear255 * alpha
                    elif "_GREEN_" in transitionCmd.type:
                        color[1] = linear255 * alpha
                    elif "_BLUE_" in transitionCmd.type:
                        color[2] = linear255 * alpha

                    color[3] = alpha
                    bpy.context.scene.node_tree.nodes["CSTrans_RGB"].outputs[0].default_value = color

        for miscCmd in csObj.ootCutsceneProperty.preview.miscList:
            startFrame = miscCmd.startFrame
            endFrame = miscCmd.endFrame

            if curFrame == startFrame:
                if miscCmd.type == "CS_MISC_SET_LOCKED_VIEWPOINT" and not None in cameraObjects:
                    bpy.context.scene.camera = cameraObjects[int(csObj.ootCutsceneProperty.preview.isFixedCamSet)]
                    csObj.ootCutsceneProperty.preview.isFixedCamSet ^= True

            if curFrame >= startFrame and curFrame <= endFrame:
                if useNodeFeatures:
                    color = [0.0, 0.0, 0.0, 0.0]
                    lerp = getLerp(endFrame, startFrame, curFrame)

                    if miscCmd.type in ["CS_MISC_VISMONO_SEPIA", "CS_MISC_VISMONO_BLACK_AND_WHITE"]:
                        if miscCmd.type == "CS_MISC_VISMONO_SEPIA":
                            col = [255.0, 180.0, 100.0]
                        else:
                            col = [255.0, 255.0, 254.0]

                        for i in range(len(col)):
                            color[i] = getColor(col[i])

                        color[3] = getColor(255.0) * lerp
                        bpy.context.scene.node_tree.nodes["CSMisc_RGB"].outputs[0].default_value = color


def cutscene_preview_register():
    bpy.app.handlers.frame_change_pre.append(cutscenePreviewFrameHandler)


def cutscene_preview_unregister():
    if cutscenePreviewFrameHandler in bpy.app.handlers.frame_change_pre:
        bpy.app.handlers.frame_change_pre.remove(cutscenePreviewFrameHandler)
