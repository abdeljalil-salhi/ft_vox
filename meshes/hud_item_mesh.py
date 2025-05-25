from typing import TYPE_CHECKING
from numpy import array, hstack, ndarray, zeros

from meshes.base_mesh import BaseMesh
from meshes.chunk_mesh_builder import pack_data

if TYPE_CHECKING:
    from srcs.engine import Engine


class HUDItemMesh(BaseMesh):
    def __init__(self, game: "Engine") -> None:
        super().__init__()

        self.game = game
        self.context = self.game.context
        self.shader = self.game.shader.chunk

        self.vbo_format = "1u4"
        self.attrs = ("packed_data",)
        self.voxel_id = 0
        self.vao = None

    def get_vertex_data(self) -> ndarray:
        # Define a cube with vertices scaled to [0, 1] range
        vertices = [
            (0, 0, 1),  # 0: Front-bottom-left
            (1, 0, 1),  # 1: Front-bottom-right
            (1, 1, 1),  # 2: Front-top-right
            (0, 1, 1),  # 3: Front-top-left
            (0, 1, 0),  # 4: Back-top-left
            (0, 0, 0),  # 5: Back-bottom-left
            (1, 0, 0),  # 6: Back-bottom-right
            (1, 1, 0),  # 7: Back-top-right
        ]

        # Define the triangles for each face of the cube
        indices = [
            # Front face
            (0, 1, 2),
            (0, 2, 3),
            # Back face
            (5, 4, 7),
            (5, 7, 6),
            # Right face
            (1, 6, 7),
            (1, 7, 2),
            # Left face
            (0, 3, 4),
            (0, 4, 5),
            # Top face
            (3, 2, 7),
            (3, 7, 4),
            # Bottom face
            (0, 5, 6),
            (0, 6, 1),
        ]

        # Create packed vertex data
        num_vertices = len(indices) * 3  # 12 triangles * 3 vertices each
        vertex_data = zeros(num_vertices, dtype="uint32")
        vertex_index = 0

        # Assign face_id based on the face being rendered
        face_ids = [
            2,
            2,  # Front face (side face, try face_id=2)
            2,
            2,  # Back face (side face)
            2,
            2,  # Right face (side face)
            2,
            2,  # Left face (side face)
            0,
            0,  # Top face (already correct)
            1,
            1,  # Bottom face (try face_id=1)
        ]

        for face_idx, triangle_group in enumerate(indices):
            if face_idx == 0 or face_idx == 1:  # Right face (indices 0 and 1)
                face_id = 2  # Side face in texture atlas
                flip_id = 1  # Flip the right face
            else:
                face_id = face_ids[face_idx]  # Use the original face_id
                flip_id = 0  # No flipping for other faces
            ao_id = 3  # No ambient occlusion for HUD items (max brightness)

            for vertex_idx in triangle_group:
                x, y, z = vertices[vertex_idx]
                # Pack the vertex data using the same format as chunk_mesh_builder
                vertex_data[vertex_index] = pack_data(
                    int(x), int(y), int(z), self.voxel_id, face_id, ao_id, flip_id
                )
                vertex_index += 1

        return vertex_data
