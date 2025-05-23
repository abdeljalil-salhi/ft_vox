from typing import TYPE_CHECKING
from numpy import array, zeros

from meshes.chunk_mesh import ChunkMesh
from settings import CHUNK_AREA, CHUNK_SIZE, CHUNK_VOLUME


if TYPE_CHECKING:
    from main import Engine


class Chunk:
    def __init__(self, game: "Engine") -> None:
        self.game = game
        self.voxels: array = self.build_voxels()
        self.mesh: ChunkMesh = None
        
        self.build_mesh()
        
    def build_mesh(self) -> None:
        self.mesh = ChunkMesh(self)
    
    def render(self) -> None:
        self.mesh.render()

    def build_voxels(self) -> array:
        voxels = zeros(CHUNK_VOLUME, dtype="uint8")

        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                for y in range(CHUNK_SIZE):
                    voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = x + y + z
        return voxels
