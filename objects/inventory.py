from objects.texturing import Texture


class Inventory:
    def __init__(self):
        self.slots = [None] * 10
        # Initialize with some items for testing
        self.slots[0] = Texture.GRASS.value
        self.slots[1] = Texture.STONE.value
        self.slots[2] = Texture.DIRT.value
        self.slots[3] = Texture.SAND.value
        self.slots[4] = Texture.WOOD.value
        self.slots[5] = Texture.TNT.value
        self.selected_slot = 0

    def select_slot(self, index):
        if 0 <= index < 10:
            self.selected_slot = index
