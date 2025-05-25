from typing import TYPE_CHECKING
from pygame import display
from glm import vec4

from meshes.hud_item_mesh import HUDItemMesh

if TYPE_CHECKING:
    from srcs.engine import Engine
    from srcs.player import Player


class HUD:
    def __init__(self, game: "Engine", player: "Player") -> None:
        self.game = game
        self.player = player
        self.hud_item_mesh = HUDItemMesh(game)

    def render(self):
        inventory = self.player.inventory
        slot_size = 50  # Size of each inventory slot in pixels
        spacing = 7  # Spacing between slots in pixels
        total_width = 10 * slot_size + 9 * spacing
        window_x = display.get_surface().get_width()
        x_start = (window_x - total_width) / 2
        y = 10  # 10 pixels from bottom

        for i in range(10):
            x = x_start + i * (slot_size + spacing)
            # Render slot background (gray)
            self.game.shader.render_2d_quad(
                x, y, slot_size, slot_size, vec4(0.5, 0.5, 0.5, 1.0)
            )
            # Render item as a 3D cube if present
            item = inventory.slots[i]
            if item is not None:
                self.game.shader.render_3d_item(
                    x + 5,
                    y + 5,
                    slot_size - 10,
                    slot_size - 10,
                    item,
                    self.hud_item_mesh,
                )
            # Render selection indicator if this is the selected slot
            if i == inventory.selected_slot:
                border_width = 2
                # Top border
                self.game.shader.render_2d_quad(
                    x - border_width,
                    y + slot_size,
                    slot_size + 2 * border_width,
                    border_width,
                    vec4(1.0, 1.0, 1.0, 1.0),
                )
                # Bottom border
                self.game.shader.render_2d_quad(
                    x - border_width,
                    y - border_width,
                    slot_size + 2 * border_width,
                    border_width,
                    vec4(1.0, 1.0, 1.0, 1.0),
                )
                # Left border
                self.game.shader.render_2d_quad(
                    x - border_width,
                    y - border_width,
                    border_width,
                    slot_size + 2 * border_width,
                    vec4(1.0, 1.0, 1.0, 1.0),
                )
                # Right border
                self.game.shader.render_2d_quad(
                    x + slot_size,
                    y - border_width,
                    border_width,
                    slot_size + 2 * border_width,
                    vec4(1.0, 1.0, 1.0, 1.0),
                )
