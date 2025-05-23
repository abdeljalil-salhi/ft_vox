from typing import TYPE_CHECKING
from glm import dot
from math import cos, tan

from objects.chunk import Chunk
from settings import CHUNK_SPHERE_RADIUS, FAR, HORIZONTAL_FOV, NEAR, VERTICAL_FOV


if TYPE_CHECKING:
    from srcs.camera import Camera


class Frustum:
    def __init__(self, camera: "Camera") -> None:
        self.camera = camera

        # Precompute factors used for horizontal and vertical plane checks
        # These are used to scale the bounding sphere check relative to the frustum angle
        self.factor_x = 1.0 / cos(half_x := HORIZONTAL_FOV * 0.5)
        self.tan_x = tan(half_x)
        self.factor_y = 1.0 / cos(half_y := VERTICAL_FOV * 0.5)
        self.tan_y = tan(half_y)

    def is_on_frustum(self, chunk: "Chunk") -> bool:
        # Vector from camera to chunk center
        sphere_vector = chunk.center - self.camera.position

        # Check if the chunk's bounding sphere is between the NEAR and FAR clipping planes
        sz = dot(sphere_vector, self.camera.forward)
        if not (NEAR - CHUNK_SPHERE_RADIUS <= sz <= FAR + CHUNK_SPHERE_RADIUS):
            return False  # Too close or too far

        # Check against TOP and BOTTOM planes
        sy = dot(sphere_vector, self.camera.up)
        distance = self.factor_y * CHUNK_SPHERE_RADIUS + sz * self.tan_y
        if not (-distance <= sy <= distance):
            return False  # Outside vertical field of view

        # Check against LEFT and RIGHT planes
        sx = dot(sphere_vector, self.camera.right)
        distance = self.factor_x * CHUNK_SPHERE_RADIUS + sz * self.tan_x
        if not (-distance <= sx <= distance):
            return False  # Outside horizontal field of view

        return True  # The chunk is inside the frustum
