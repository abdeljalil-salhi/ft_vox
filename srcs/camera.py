from typing import TYPE_CHECKING
from glm import (
    vec3,
    ivec3,
    radians,
    perspective,
    mat4,
    cos,
    sin,
    normalize,
    cross,
    lookAt,
    clamp,
)
from math import floor

from settings import (
    GO_THROUGH,
    VERTICAL_FOV,
    ASPECT_RATIO,
    NEAR,
    FAR,
    PITCH_LIMIT,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    PLAYER_DEPTH,
    EYE_HEIGHT,
    COLLISION_OFFSET,
)
from srcs.frustum import Frustum

if TYPE_CHECKING:
    from srcs.world import World


class Camera:
    """
    A 3D first-person camera class for a voxel-based engine.

    The Camera handles position, orientation (yaw/pitch), movement with collision detection,
    and view/projection matrix computation for rendering.

    It maintains local axes (`forward`, `right`, `up`) and updates them based on rotation.
    The camera also supports Axis-Aligned Bounding Box (AABB) collision.
    """

    def __init__(self, position: float, yaw: float, pitch: float) -> None:
        """
        Initialize the camera with a position and rotation angles.

        Args:
            position (float): Initial position of the camera.
            yaw (float): Initial yaw angle in degrees.
            pitch (float): Initial pitch angle in degrees.
        """
        self.position = vec3(position)
        self.yaw = radians(yaw)
        self.pitch = radians(pitch)

        self.up = vec3(0.0, 1.0, 0.0)
        self.right = vec3(1.0, 0.0, 0.0)
        self.forward = vec3(0.0, 0.0, -1.0)

        self.matrix_projection = perspective(VERTICAL_FOV, ASPECT_RATIO, NEAR, FAR)
        self.matrix_view = mat4()

        self.frustum = Frustum(self)

    def update(self) -> None:
        """
        Update camera direction vectors and view matrix.
        Should be called every frame before rendering.
        """
        self.update_vectors()
        self.update_view_matrix()

    def update_view_matrix(self) -> None:
        """
        Recalculate the view matrix using the current position and orientation.
        Eye height is added to simulate a player's viewpoint.
        """
        eye_position = self.position + vec3(0, EYE_HEIGHT, 0)
        self.matrix_view = lookAt(eye_position, eye_position + self.forward, self.up)

    def update_vectors(self) -> None:
        """
        Update direction vectors (`forward`, `right`, `up`) based on yaw and pitch angles.
        """
        self.forward.x = cos(self.yaw) * cos(self.pitch)
        self.forward.y = sin(self.pitch)
        self.forward.z = sin(self.yaw) * cos(self.pitch)

        self.forward = normalize(self.forward)
        self.right = normalize(cross(self.forward, vec3(0.0, 1.0, 0.0)))
        self.up = normalize(cross(self.right, self.forward))

    def rotate_pitch(self, delta_y: float) -> None:
        """
        Rotate the camera pitch (up/down) and clamp it within allowed limits.

        Args:
            delta_y (float): Amount to change the pitch.
        """
        self.pitch -= delta_y
        self.pitch = clamp(self.pitch, -PITCH_LIMIT, PITCH_LIMIT)

    def rotate_yaw(self, delta_x: float) -> None:
        """
        Rotate the camera yaw (left/right).

        Args:
            delta_x (float): Amount to change the yaw.
        """
        self.yaw += delta_x

    def is_position_valid(self, position: vec3) -> bool:
        """
        Check whether a player's bounding box (AABB) at the given position
        collides with any solid voxel in the world.

        Args:
            position (vec3): Proposed new position.

        Returns:
            bool: True if position is valid (no collision), False otherwise.
        """
        min_x = position.x - PLAYER_WIDTH / 2
        max_x = position.x + PLAYER_WIDTH / 2
        min_y = position.y + COLLISION_OFFSET
        max_y = position.y + PLAYER_HEIGHT
        min_z = position.z - PLAYER_DEPTH / 2
        max_z = position.z + PLAYER_DEPTH / 2

        i_min, i_max = floor(min_x), floor(max_x)
        j_min, j_max = floor(min_y), floor(max_y)
        k_min, k_max = floor(min_z), floor(max_z)

        for i in range(i_min, i_max + 1):
            for j in range(j_min, j_max + 1):
                for k in range(k_min, k_max + 1):
                    if self.world.voxel_handler.get_voxel_id(ivec3(i, j, k))[0] != 0:
                        return False
        return True

    def move(
        self, forward_velocity: float, right_velocity: float, up_velocity: float
    ) -> None:
        """
        Attempt to move the camera, handling sliding on blocked axes.

        Args:
            forward_velocity (float): Movement in the forward/backward direction.
            right_velocity (float): Movement in the right/left direction.
            up_velocity (float): Movement in the up/down direction.
        """
        desired_movement = (
            self.forward * forward_velocity
            + self.right * right_velocity
            + self.up * up_velocity
        )

        new_position = self.position + desired_movement

        if self.is_position_valid(new_position) or GO_THROUGH:
            self.position = new_position
            return

        movement = vec3(0, 0, 0)

        # Try X-axis
        if desired_movement.x != 0:
            x_position = self.position + vec3(desired_movement.x, 0, 0)
            if self.is_position_valid(x_position):
                movement.x = desired_movement.x

        # Try Y-axis
        if desired_movement.y != 0:
            y_position = self.position + vec3(0, desired_movement.y, 0)
            if self.is_position_valid(y_position):
                movement.y = desired_movement.y

        # Try Z-axis
        if desired_movement.z != 0:
            z_position = self.position + vec3(0, 0, desired_movement.z)
            if self.is_position_valid(z_position):
                movement.z = desired_movement.z

        # Apply allowed movement
        self.position += movement

    # Movement convenience methods
    def move_forward(self, velocity: float) -> None:
        """Move the camera forward."""
        self.move(velocity, 0, 0)

    def move_backward(self, velocity: float) -> None:
        """Move the camera backward."""
        self.move(-velocity, 0, 0)

    def move_right(self, velocity: float) -> None:
        """Strafe the camera to the right."""
        self.move(0, velocity, 0)

    def move_left(self, velocity: float) -> None:
        """Strafe the camera to the left."""
        self.move(0, -velocity, 0)

    def move_up(self, velocity: float) -> None:
        """Move the camera upward."""
        self.move(0, 0, velocity)

    def move_down(self, velocity: float) -> None:
        """Move the camera downward."""
        self.move(0, 0, -velocity)
