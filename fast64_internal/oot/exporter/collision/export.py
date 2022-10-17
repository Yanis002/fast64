from mathutils import Matrix, Vector
from math import pi
from bpy.types import Object, Mesh
from bpy.ops import object
from ....utility import PluginError
from ...panel.properties.collision import OOTMaterialCollisionProperty
from ..classes import OOTCollision, OOTCollisionVertex, OOTCollisionPolygon, OOTPolygonType
from ..utility import convertIntTo2sComplement, getCustomProperty


def getPolygonType(collisionProp: OOTMaterialCollisionProperty):
    polygonType = OOTPolygonType()
    polygonType.ignoreCameraCollision = collisionProp.ignoreCameraCollision
    polygonType.ignoreActorCollision = collisionProp.ignoreActorCollision
    polygonType.ignoreProjectileCollision = collisionProp.ignoreProjectileCollision
    polygonType.eponaBlock = collisionProp.eponaBlock
    polygonType.decreaseHeight = collisionProp.decreaseHeight
    polygonType.floorSetting = getCustomProperty(collisionProp, "floorSetting")
    polygonType.wallSetting = getCustomProperty(collisionProp, "wallSetting")
    polygonType.floorProperty = getCustomProperty(collisionProp, "floorProperty")
    polygonType.exitID = collisionProp.exitID
    polygonType.cameraID = collisionProp.cameraID
    polygonType.isWallDamage = collisionProp.isWallDamage
    polygonType.enableConveyor = collisionProp.conveyorOption == "Land"

    if collisionProp.conveyorOption != "None":
        polygonType.conveyorRotation = int(collisionProp.conveyorRotation / (2 * pi) * 0x3F)
        polygonType.conveyorSpeed = int(getCustomProperty(collisionProp, "conveyorSpeed"), 16) + (
            4 if collisionProp.conveyorKeepMomentum else 0
        )
    else:
        polygonType.conveyorRotation = 0
        polygonType.conveyorSpeed = 0

    polygonType.hookshotable = collisionProp.hookshotable
    polygonType.echo = collisionProp.echo
    polygonType.lightingSetting = collisionProp.lightingSetting
    polygonType.terrain = getCustomProperty(collisionProp, "terrain")
    polygonType.sound = getCustomProperty(collisionProp, "sound")

    return polygonType


def roundPosition(position: list[int]):
    return (round(position[0]), round(position[1]), round(position[2]))


def collisionVertIndex(vert: int, vertArray: list[OOTCollisionVertex]):
    for i in range(len(vertArray)):
        colVert = vertArray[i]

        if colVert.position == vert:
            return i

    return None


def updateBounds(position: list[int], bounds: list[int]):
    if len(bounds) > 0:
        minBounds = bounds[0]
        maxBounds = bounds[1]

        for i in range(3):
            if position[i] < minBounds[i]:
                minBounds[i] = position[i]

            if position[i] > maxBounds[i]:
                maxBounds[i] = position[i]
    else:
        bounds.append([position[0], position[1], position[2]])
        bounds.append([position[0], position[1], position[2]])


def addCollisionTriangles(
    obj: Object,
    collisionDict: dict[OOTPolygonType, list],
    includeChildren: bool,
    transformMatrix: Matrix,
    bounds: list[int],
):
    if isinstance(obj.data, Mesh) and not obj.ignore_collision:
        if len(obj.data.materials) > 0:
            obj.data.calc_loop_triangles()

            for face in obj.data.loop_triangles:
                material = obj.material_slots[face.material_index].material
                polygonType = getPolygonType(material.ootCollisionProperty)

                planePoint = transformMatrix @ obj.data.vertices[face.vertices[0]].co
                (x1, y1, z1) = roundPosition(planePoint)
                (x2, y2, z2) = roundPosition(transformMatrix @ obj.data.vertices[face.vertices[1]].co)
                (x3, y3, z3) = roundPosition(transformMatrix @ obj.data.vertices[face.vertices[2]].co)

                updateBounds((x1, y1, z1), bounds)
                updateBounds((x2, y2, z2), bounds)
                updateBounds((x3, y3, z3), bounds)

                faceNormal = (transformMatrix.inverted().transposed() @ face.normal).normalized()
                distance = int(
                    round(
                        -1
                        * (
                            faceNormal[0] * planePoint[0]
                            + faceNormal[1] * planePoint[1]
                            + faceNormal[2] * planePoint[2]
                        )
                    )
                )
                distance = convertIntTo2sComplement(distance, 2, True)

                nx = (y2 - y1) * (z3 - z2) - (z2 - z1) * (y3 - y2)
                ny = (z2 - z1) * (x3 - x2) - (x2 - x1) * (z3 - z2)
                nz = (x2 - x1) * (y3 - y2) - (y2 - y1) * (x3 - x2)
                magSqr = nx * nx + ny * ny + nz * nz

                if magSqr > 0:
                    if polygonType not in collisionDict:
                        collisionDict[polygonType] = []

                    positions = ((x1, y1, z1), (x2, y2, z2), (x3, y3, z3))
                    collisionDict[polygonType].append((positions, faceNormal, distance))
                else:
                    print("Ignore denormalized triangle.")
        else:
            raise PluginError(f"Object: '{obj.name}' must have a material associated with it.")

    if includeChildren:
        for child in obj.children:
            addCollisionTriangles(child, collisionDict, includeChildren, transformMatrix @ child.matrix_local, bounds)


def exportCollisionCommon(collision: OOTCollision, obj: Object, transformMatrix: Matrix, includeChildren: bool):
    object.select_all(action="DESELECT")
    obj.select_set(True)

    # dict of collisionType : faces
    collisionDict: dict[OOTPolygonType, list] = {}

    addCollisionTriangles(obj, collisionDict, includeChildren, transformMatrix, collision.bounds)
    for polygonType, faces in collisionDict.items():
        collision.polygonGroups[polygonType] = []

        for (faceVerts, normal, distance) in faces:
            assert len(faceVerts) == 3
            indices = []

            for roundedPosition in faceVerts:
                index = collisionVertIndex(roundedPosition, collision.vertices)

                if index is None:
                    collision.vertices.append(OOTCollisionVertex(roundedPosition))
                    indices.append(len(collision.vertices) - 1)
                else:
                    indices.append(index)

            assert len(indices) == 3

            # We need to ensure two things about the order in which the vertex indices are:
            #
            # 1) The vertex with the minimum y coordinate should be first.
            # This prevents a bug due to an optimization in OoT's CollisionPoly_GetMinY.
            # https://github.com/zeldaret/oot/blob/7996df1913bcf47095f972534385fcdd0bafeb6e/src/code/z_bgcheck.c#L208
            #
            # 2) The vertices should wrap around the polygon normal **counter-clockwise**.
            # This is needed for OoT's dynapoly, which is collision that can move.
            # When it moves, the vertex coordinates and normals are recomputed.
            # The normal is computed based on the vertex coordinates, which makes the order of vertices matter.
            # https://github.com/zeldaret/oot/blob/7996df1913bcf47095f972534385fcdd0bafeb6e/src/code/z_bgcheck.c#L2973

            # Address 1): sort by ascending y coordinate
            indices.sort(key=lambda index: collision.vertices[index].position[1])

            # Address 2):
            # swap indices[1] and indices[2],
            # if the normal computed from the vertices in the current order is the wrong way.
            v0 = Vector(collision.vertices[indices[0]].position)
            v1 = Vector(collision.vertices[indices[1]].position)
            v2 = Vector(collision.vertices[indices[2]].position)

            if (v1 - v0).cross(v2 - v0).dot(Vector(normal)) < 0:
                indices[1], indices[2] = indices[2], indices[1]

            collision.polygonGroups[polygonType].append(OOTCollisionPolygon(indices, normal, distance))
