from typing import TYPE_CHECKING
from numpy import hstack

from meshes.base_mesh import BaseMesh

if TYPE_CHECKING:
    from srcs.engine import Engine


class QuadMesh(BaseMesh):
    def __init__(self, game: "Engine") -> None:
        super().__init__()

        self.game = game
        self.context = self.game.context
        self.shader = self.game.shader.quad

        self.vbo_format = "3f 3f"
        self.attrs = ("in_position", "in_color")
        self.vao = self.get_vao()

    def get_vertex_data(self):
        vertices = [
            (0.5, 0.5, 0.0),
            (-0.5, 0.5, 0.0),
            (-0.5, -0.5, 0.0),
            (0.5, 0.5, 0.0),
            (-0.5, -0.5, 0.0),
            (0.5, -0.5, 0.0),
        ]
        colors = [(0, 1, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (1, 1, 0), (0, 0, 1)]
        vertex_data = hstack([vertices, colors], dtype="float32")
        return vertex_data
