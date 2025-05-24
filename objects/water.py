from typing import TYPE_CHECKING

from meshes.water_mesh import WaterMesh

if TYPE_CHECKING:
    from main import Engine


class Water:
    def __init__(self, game: "Engine") -> None:
        self.game = game
        self.mesh = WaterMesh(game)

    def render(self) -> None:
        self.mesh.render()
