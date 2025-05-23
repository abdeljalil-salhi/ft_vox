from typing import TYPE_CHECKING
from moderngl import CULL_FACE

from meshes.quad_mesh import QuadMesh

if TYPE_CHECKING:
    from main import Engine


class Scene:
    def __init__(self, game: "Engine") -> None:
        self.game = game
        self.quad = QuadMesh(self.game)

    def update(self) -> None:
        pass

    def render(self) -> None:
        self.quad.render()
