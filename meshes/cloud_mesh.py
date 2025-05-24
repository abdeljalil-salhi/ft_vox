from typing import TYPE_CHECKING
from numba import njit
from numpy import empty, ndarray, zeros

from meshes.base_mesh import BaseMesh
from objects.texturing import CLOUD_HEIGHT
from settings import CHUNK_AREA, CHUNK_SIZE, WORLD_AREA, WORLD_DEPTH, WORLD_WIDTH
from srcs.noise import noise2

if TYPE_CHECKING:
    from srcs.engine import Engine


class CloudMesh(BaseMesh):
    """
    A class responsible for generating and rendering a mesh of clouds in the sky.
    """

    def __init__(self, game: "Engine") -> None:
        super().__init__()
        self.game = game
        self.context = self.game.context
        self.shader = self.game.shader.clouds
        self.vbo_format = "3u2"
        self.attrs = ("in_position",)
        self.vao = self.get_vao()

    def get_vertex_data(self) -> ndarray:
        """
        Fills a data array with cloud presence (0 or 1), then builds mesh data.

        Returns:
            ndarray: A 1D array of vertex data representing the cloud mesh.
        """
        # Create an array to store whether a cloud exists at each block
        cloud_data = zeros(WORLD_AREA * CHUNK_SIZE**2, dtype="uint8")

        # Fill this array using noise to simulate cloud coverage
        self.generate_clouds(cloud_data)

        # Convert cloud data into vertex data (mesh)
        return self.build_mesh(cloud_data)

    @staticmethod
    @njit
    def generate_clouds(cloud_data: ndarray) -> None:
        """
        @staticmethod @njit

        Populate `cloud_data` array with 1s where clouds should be generated,
        using 2D noise to determine cloud coverage.

        Args:
            cloud_data (ndarray): An array to fill with cloud presence (1 for cloud, 0 for no cloud).
        """
        for x in range(WORLD_WIDTH * CHUNK_SIZE):
            for z in range(WORLD_DEPTH * CHUNK_SIZE):
                # Skip this spot if noise is below a certain threshold (less likely to have clouds)
                if noise2(0.13 * x, 0.13 * z) < 0.2:
                    continue
                cloud_data[x + WORLD_WIDTH * CHUNK_SIZE * z] = (
                    1  # Mark this block for cloud
                )

    @staticmethod
    @njit
    def build_mesh(cloud_data: ndarray) -> ndarray:
        """
        @staticmethod @njit

        Converts `cloud_data` into a list of large flat quads (2D rectangles)
        to optimize rendering. Each quad is made of 2 triangles (6 vertices).

        Args:
            cloud_data (ndarray): An array indicating where clouds are present (1 for cloud, 0 for no cloud).

        Returns:
            ndarray: A filled 1D array of vertex data representing the cloud mesh.
        """
        # Preallocate space for the mesh (max size)
        mesh = empty(WORLD_AREA * CHUNK_AREA * 6 * 3, dtype="uint16")
        index = 0  # Current write position in the mesh array

        width = WORLD_WIDTH * CHUNK_SIZE
        depth = WORLD_DEPTH * CHUNK_SIZE
        y = CLOUD_HEIGHT  # All clouds are rendered at the same Y height

        visited = set()  # Keep track of already processed cloud blocks

        for z in range(depth):
            for x in range(width):
                idx = x + width * z

                # Skip if there's no cloud here or this block has already been used
                if not cloud_data[idx] or idx in visited:
                    continue

                # Try to extend the quad in the X direction as far as possible
                x_count = 1
                idx = (x + x_count) + width * z
                while x + x_count < width and cloud_data[idx] and idx not in visited:
                    x_count += 1
                    idx = (x + x_count) + width * z

                # For each X, try to extend the quad in the Z direction
                z_count_list = []
                for ix in range(x_count):
                    z_count = 1
                    idx = (x + ix) + width * (z + z_count)
                    while (
                        (z + z_count) < depth and cloud_data[idx] and idx not in visited
                    ):
                        z_count += 1
                        idx = (x + ix) + width * (z + z_count)
                    z_count_list.append(z_count)

                # Use the smallest Z extension across all Xs to make a uniform quad
                z_count = min(z_count_list) if z_count_list else 1

                # Mark all blocks in this quad as visited so they’re not used again
                for ix in range(x_count):
                    for iz in range(z_count):
                        visited.add((x + ix) + width * (z + iz))

                # Define the corners of the quad (v0 through v3)
                v0 = x, y, z
                v1 = x + x_count, y, z + z_count
                v2 = x + x_count, y, z
                v3 = x, y, z + z_count

                # Create two triangles from the quad and store their vertices
                for vertex in (v0, v1, v2, v0, v3, v1):
                    for attr in vertex:
                        mesh[index] = attr
                        index += 1

        # Return only the filled part of the mesh array
        return mesh[: index + 1]
