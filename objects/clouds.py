from typing import TYPE_CHECKING

from meshes.cloud_mesh import CloudMesh
from objects.texturing import CLOUD_COLOR

if TYPE_CHECKING:
    from srcs.engine import Engine


class Clouds:
    """
    Manages the cloud system in the game world.
    Handles cloud updates and rendering.
    """

    def __init__(self, game: "Engine") -> None:
        self.game = game

        # Create the cloud mesh object, responsible for generating and rendering cloud geometry
        self.mesh = CloudMesh(game)

    def update(self) -> None:
        """
        Update the cloud shader with the current game time.
        This allows clouds to animate or shift over time.
        """
        self.mesh.shader["unit_time"] = self.game.time
        self.mesh.shader["cloud_color"] = CLOUD_COLOR

    def render(self) -> None:
        """
        Render the clouds by calling the mesh's render function.
        """
        self.mesh.render()
