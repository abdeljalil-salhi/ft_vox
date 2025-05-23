import random
from typing import TYPE_CHECKING
from glm import ivec3, mat4, simplex, vec2, vec3, translate
from numpy import array, ndarray, zeros

from meshes.chunk_mesh import ChunkMesh
from settings import CHUNK_AREA, CHUNK_SIZE, CHUNK_VOLUME, SHOW_CHUNKS


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
        chunk_color = random.randrange(1, 100)

        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                wx = cx + x
                wz = cz + z
                world_height = int(simplex(vec2(wx, wz) * 0.01) * 32 + 32)
                local_height = min(world_height - cy, CHUNK_SIZE)

                for y in range(local_height):
                    wy = y + cy
                    voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = (
                        chunk_color if SHOW_CHUNKS else wy + 1
                    )

        if any(voxels):
            self.is_empty = False

        return voxels
