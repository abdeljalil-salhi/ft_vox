from enum import Enum
from glm import vec3

from settings import CHUNK_SIZE, WORLD_WIDTH


# Color constants
SKYBOX_COLOR = vec3(0.58, 0.83, 0.99)


# Textures IDs
class Texture(Enum):
    SAND = 1
    GRASS = 2
    DIRT = 3
    STONE = 4
    SNOW = 5
    SAKURA_LEAVES = 6
    WOOD = 7
    TNT = 8
    OAK_PLANK = 9
    DIAMOND_ORE = 10
    NORMAL_LEAVES = 11
    BEEHIVE = 12
    OAK_LEAVES = 13
    GOLD_BLOCK = 14


# Terrain levels
class TerrainLevel(Enum):
    SAND = 7
    GRASS = 8
    DIRT = 40
    STONE = 49
    SNOW = 54


# Tree settings
TREE_PROBABILITY = 0.02
TREE_WIDTH, TREE_HEIGHT = 4, 8
TREE_H_WIDTH, TREE_H_HEIGHT = TREE_WIDTH // 2, TREE_HEIGHT // 2


# Water settings
WATER_LINE = 5.8
WATER_AREA = 5 * CHUNK_SIZE * WORLD_WIDTH
