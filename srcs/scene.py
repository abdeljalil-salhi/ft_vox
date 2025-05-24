from typing import TYPE_CHECKING

from moderngl import CULL_FACE

from objects.voxel_marker import VoxelMarker
from objects.water import Water
from srcs.world import World

if TYPE_CHECKING:
    from srcs.engine import Engine


class Scene:
    def __init__(self, game: "Engine") -> None:
        self.game = game
        self.world = World(self.game)
        self.voxel_marker = VoxelMarker(self.world.voxel_handler)
        self.water = Water(self.game)

    def update(self) -> None:
        self.world.update()
        self.voxel_marker.update()

    def render(self) -> None:
        # Rendering the chunks
        self.world.render()
        
        # Rendering water without cull facing
        self.game.context.disable(CULL_FACE)
        self.water.render()
        self.game.context.enable(CULL_FACE)
        
        # Rendering voxel marker
        self.voxel_marker.render()
