from typing import TYPE_CHECKING

from meshes.base_mesh import BaseMesh
from meshes.chunk_mesh_builder import build_chunk_mesh

if TYPE_CHECKING:
    from objects.chunk import Chunk


class ChunkMesh(BaseMesh):
    def __init__(self, chunk: "Chunk") -> None:
        super().__init__()
        self.game = chunk.game
        self.chunk = chunk
        self.context = self.game.context
        self.shader = self.game.shader.chunk

        self.vbo_format = "1u4"
        self.format_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())
        self.attrs = ("packed_data",)
        self.vao = self.get_vao()

    def rebuild(self) -> None:
        self.vao = self.get_vao()

    def get_vertex_data(self):
        mesh = build_chunk_mesh(
            self.chunk.voxels,
            self.format_size,
            self.chunk.position,
            self.chunk.world.voxels,
        )
        return mesh
