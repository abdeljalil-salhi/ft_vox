from typing import TYPE_CHECKING
from glm import mat4, simplex, vec3, translate
from numpy import array, ndarray, zeros

from meshes.chunk_mesh import ChunkMesh
from settings import CHUNK_AREA, CHUNK_SIZE, CHUNK_VOLUME


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

    def get_model_matrix(self) -> ndarray:
        return translate(mat4(), vec3(self.position) * CHUNK_SIZE)

    def set_uniform(self) -> None:
        self.mesh.shader["matrix_model"].write(self.matrix_model)

    def build_mesh(self) -> None:
        self.mesh = ChunkMesh(self)

    def render(self) -> None:
        self.set_uniform()
        self.mesh.render()

    def build_voxels(self) -> ndarray:
        voxels = zeros(CHUNK_VOLUME, dtype="uint8")

        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                for y in range(CHUNK_SIZE):
                    voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = (
                        x + y + z if int(simplex(vec3(x, y, z) * 0.1) + 1) else 0
                    )
        return voxels
