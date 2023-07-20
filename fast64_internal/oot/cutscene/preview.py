import bpy

from bpy.types import Scene, Object
from bpy.app.handlers import persistent
from ...utility import gammaInverse


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
        print("ERROR: This version of Blender do not have support for Viewport Compositor Nodes")
        return None, None

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

    nodeTree = bpy.context.scene.node_tree

    if bpy.context.scene.ootCSPreviewNodesReady:
        return nodeTree.nodes["CSTrans_RGB"], nodeTree.nodes["CSTrans_AlphaOver"]
    
    nodeRenderLayer = nodeComposite = nodeRGB = nodeAlphaOver = None
    for node in nodeTree.nodes.values():
        # print(node.type)
        if node.type == "R_LAYERS":
            nodeRenderLayer = node

        if node.type == "COMPOSITE":
            nodeComposite = node

        if node.type == "RGB":
            nodeRGB = node

        if node.type == "ALPHA_OVER":
            nodeAlphaOver = node

    if nodeRenderLayer is None:
        nodeRenderLayer = nodeTree.nodes.new("CompositorNodeRLayers")
    nodeRenderLayer.select = False
    nodeRenderLayer.name = nodeRenderLayer.label = "CSTrans_RenderLayer"
    nodeRenderLayer.location = (-330, 0)

    if nodeComposite is None:
        nodeComposite = nodeTree.nodes.new("CompositorNodeComposite")
    nodeComposite.select = True
    nodeComposite.name = nodeComposite.label = "CSTrans_Composite"
    nodeComposite.location = (300, 0)

    if nodeRGB is None:
        nodeRGB = nodeTree.nodes.new("CompositorNodeRGB")
    nodeRGB.select = False
    nodeRGB.name = nodeRGB.label = "CSTrans_RGB"
    nodeRGB.location = (-60, 0)

    if nodeAlphaOver is None:
        nodeAlphaOver = nodeTree.nodes.new("CompositorNodeAlphaOver")
    nodeAlphaOver.select = False
    nodeAlphaOver.name = nodeAlphaOver.label = "CSTrans_AlphaOver"
    nodeAlphaOver.location = (120, 0)
    nodeAlphaOver.inputs[0].default_value = 1.0

    nodeTree.links.new(nodeAlphaOver.inputs[1], nodeRenderLayer.outputs[0])
    nodeTree.links.new(nodeComposite.inputs[0], nodeAlphaOver.outputs[0])
    nodeTree.links.new(nodeAlphaOver.inputs[2], nodeRGB.outputs[0])

    bpy.context.scene.ootCSPreviewNodesReady = True
    return nodeRGB, nodeAlphaOver


@persistent
def cutscenePreviewFrameHandler(scene: Scene):
    csObj = None

    for obj in bpy.data.objects:
        if obj == bpy.context.scene.camera and obj.parent is not None:
            csObj = obj.parent
            break

    if csObj is None or not csObj.type == "EMPTY" and not csObj.ootEmptyType == "Cutscene":
        print("ERROR: Current Object is not a cutscene!")
        return

    nodeRGB, nodeAlphaOver = setupCompositorNodes()

    if not bpy.context.scene.ootCSPreviewNodesReady:
        print("ERROR: Nodes aren't ready!")

    if nodeRGB is None or nodeAlphaOver is None:
        return

    # Simulate cutscene for all frames up to present
    for curFrame in range(bpy.context.scene.frame_current):
        if curFrame == 0:
            color = [0.0, 0.0, 0.0, 0.0]

            if "link_home" in csObj.name:
                # special case for link's house because of the entrance table
                color[3] = 1.0

            bpy.context.scene.node_tree.nodes["CSTrans_RGB"].outputs[0].default_value = color
            curFrame += 1

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


def cutscene_preview_register():
    bpy.app.handlers.frame_change_pre.append(cutscenePreviewFrameHandler)


def cutscene_preview_unregister():
    if cutscenePreviewFrameHandler in bpy.app.handlers.frame_change_pre:
        bpy.app.handlers.frame_change_pre.remove(cutscenePreviewFrameHandler)
