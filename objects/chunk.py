from typing import TYPE_CHECKING
from glm import ivec3, mat4, vec3, translate
from numpy import ndarray, zeros, any
from numba import njit

from meshes.chunk_mesh import ChunkMesh
from settings import CHUNK_SIZE, CHUNK_VOLUME
from srcs.terrain_generation import get_height, set_voxel_id


if TYPE_CHECKING:
    from srcs.world import World


class Chunk:
    def __init__(self, world: "World", position: tuple) -> None:
        self.game = world.game
        self.world = world
        self.position = position
        self.matrix_model = self.get_model_matrix()
        self.voxels: ndarray = None
        self.mesh: ChunkMesh = None
        self.is_empty = True

        self.center = (vec3(self.position) + 0.5) * CHUNK_SIZE
        self.is_on_frustum = self.game.player.frustum.is_on_frustum

    def get_model_matrix(self) -> ndarray:
        return translate(mat4(), vec3(self.position) * CHUNK_SIZE)

    def set_uniform(self) -> None:
        self.mesh.shader["matrix_model"].write(self.matrix_model)

    def build_mesh(self) -> None:
        self.mesh = ChunkMesh(self)

    def render(self) -> None:
        if self.is_empty or not self.is_on_frustum(self):
            return
        self.set_uniform()
        self.mesh.render()

    def build_voxels(self) -> ndarray:
        voxels = zeros(CHUNK_VOLUME, dtype="uint8")

        cx, cy, cz = ivec3(self.position) * CHUNK_SIZE

        self.generate_terrain(voxels, cx, cy, cz)

        if any(voxels):
            self.is_empty = False

        return voxels

    @staticmethod
    @njit
    def generate_terrain(voxels: ndarray, cx: int, cy: int, cz: int) -> None:
        for x in range(CHUNK_SIZE):
            wx = cx + x
            for z in range(CHUNK_SIZE):
                wz = cz + z
                world_height = get_height(wx, wz)
                local_height = min(world_height - cy, CHUNK_SIZE)

                for y in range(local_height):
                    wy = y + cy
                    set_voxel_id(voxels, x, y, z, wx, wy, wz, world_height)
