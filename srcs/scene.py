from typing import TYPE_CHECKING

from moderngl import CULL_FACE, DEPTH_TEST

from objects.hud import HUD
from objects.clouds import Clouds
from objects.voxel_marker import VoxelMarker
from objects.water import Water
from srcs.world import World

if TYPE_CHECKING:
    from srcs.engine import Engine


class Scene:
    """
    Represents everything visible and interactive in the game world.
    Manages and updates world chunks, clouds, water, and markers.
    """

    def __init__(self, game: "Engine") -> None:
        self.game = game

        # Create the world which contains all terrain and chunk data
        self.world = World(self.game)

        # Create the HUD (heads-up display) for player stats, inventory, etc.
        self.hud = HUD(self.game, self.game.player)

        # Create the voxel marker (e.g., for block highlighting/placement)
        self.voxel_marker = VoxelMarker(self.world.voxel_handler)

        # Create water system (water surface rendering)
        self.water = Water(self.game)

        # Create cloud system (procedural sky clouds)
        self.clouds = Clouds(self.game)

    def update(self) -> None:
        """
        Update the game world and all its dynamic components.
        Called once every frame before rendering.
        """
        self.world.update()  # Update world state (e.g., chunk loading, animations)
        self.voxel_marker.update()  # Update voxel marker position/visibility
        self.clouds.update()  # Update clouds (e.g., animated movement)

    def render(self) -> None:
        """
        Render all components of the scene in the correct order.
        """

        # Render world terrain/chunks (opaque geometry first)
        self.world.render()

        # Disable back-face culling so clouds and water render fully
        self.game.context.disable(CULL_FACE)

        # Render procedural clouds and water surface
        # Clouds are rendered without culling to ensure they are always visible
        self.clouds.render()
        self.water.render()

        # Re-enable face culling for performance (for next objects)
        self.game.context.enable(CULL_FACE)

        # Render voxel marker (e.g., highlighted block under the cursor)
        self.voxel_marker.render()

        self.game.context.disable(DEPTH_TEST)  # Disable depth test for 2D HUD rendering
        # Render the HUD (heads-up display) on top of everything else
        self.hud.render()
        self.game.context.enable(DEPTH_TEST)  # Re-enable if needed
