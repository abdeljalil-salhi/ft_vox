from typing import TYPE_CHECKING
from glm import vec3, translate, mat4x4, mat4

from meshes.cube_mesh import CubeMesh

if TYPE_CHECKING:
    from srcs.voxel_handler import VoxelHandler


class VoxelMarker:
    def __init__(self, voxel_handler: "VoxelHandler") -> None:
        self.handler = voxel_handler
        self.game = self.handler.game
        self.position = vec3(0.0)  # Initial position of the marker (default at origin)
        self.matrix_model = (
            self.get_model_matrix()
        )  # Initial model matrix (based on position)
        self.mesh = CubeMesh(
            self.game
        )  # The mesh that visually represents the marker (a cube)

    def update(self) -> None:
        # Update the position of the marker if a voxel is targeted
        if self.handler.voxel_id:
            if self.handler.interaction_mode:
                # If interaction mode is active (e.g. placing a voxel),
                # move the marker one unit in the direction of the surface normal
                self.position = (
                    self.handler.voxel_world_position + self.handler.voxel_normal
                )
            else:
                # If not interacting (e.g. highlighting),
                # the marker is placed directly on the targeted voxel
                self.position = self.handler.voxel_world_position

    def set_uniform(self) -> None:
        # Set shader uniforms before rendering:
        # 1. Pass the interaction mode (0 or 1) to control marker color
        # 2. Update the model matrix to match the marker's current position
        self.mesh.shader["mode_id"] = self.handler.interaction_mode
        self.mesh.shader["matrix_model"].write(self.get_model_matrix())

    def get_model_matrix(self) -> mat4x4:
        # Construct and return the model matrix using the marker's position
        # This is used to translate the marker mesh in 3D space
        return translate(mat4(), vec3(self.position))

    def render(self) -> None:
        # Render the marker only if a voxel is being hovered over or interacted with
        if self.handler.voxel_id:
            self.set_uniform()
            self.mesh.render()
