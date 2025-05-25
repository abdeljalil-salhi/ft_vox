from typing import TYPE_CHECKING
from objects.texturing import Texture


if TYPE_CHECKING:
    from srcs.engine import Engine


class Inventory:
    def __init__(self, game: "Engine") -> None:
        self.game = game
        self.player = game.player

        self.slots = [None] * 10
        # Initialize with some items for testing
        self.slots[0] = Texture.GRASS.value
        self.slots[1] = Texture.STONE.value
        self.slots[2] = Texture.DIRT.value
        self.slots[3] = Texture.SAND.value
        self.slots[4] = Texture.WOOD.value
        self.slots[5] = Texture.TNT.value
        self.selected_slot = 0

    def select_slot(self, index: int) -> None:
        """Selects a slot in the inventory."""
        if 0 <= index < 10:
            self.selected_slot = index

    def get_selected_item(self) -> Texture:
        """Returns the currently selected item."""
        return (
            self.slots[self.selected_slot] if self.slots[self.selected_slot] else 0
        )
