from enum import Enum
from glm import vec3

from settings import CHUNK_SIZE, WORLD_HEIGHT, WORLD_WIDTH


# Color constants
SKYBOX_COLOR = vec3(0.58, 0.83, 0.99)


# Textures IDs
class Texture(Enum):
    """
    Enum representing different texture IDs used in the game.
    """

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
    """
    Enum representing different terrain levels in the game.
    """

    SAND = 7
    GRASS = 8
    DIRT = 40
    STONE = 49
    SNOW = 54


# Tree settings
TREE_PROBABILITY = 0.02
TREE_WIDTH, TREE_HEIGHT = 4, 8
TREE_H_WIDTH, TREE_H_HEIGHT = TREE_WIDTH // 2, TREE_HEIGHT // 2

BEEHIVE_PROBABILITY = 0.03


# Water settings
WATER_LINE = 5.8
WATER_AREA = 5 * CHUNK_SIZE * WORLD_WIDTH


# Cloud settings
CLOUD_COLOR = vec3(1.0, 1.0, 1.0)
CLOUD_SCALE = 25
CLOUD_HEIGHT = WORLD_HEIGHT * CHUNK_SIZE * 2

# Cluster parameters
CLUSTER_FREQUENCY = 0.05  # Frequency changes every 50 voxels (higher = more frequent)
CLUSTER_THRESHOLD = (
    0.8  # Threshold for placing a cluster; > 0.8 in [-1, 1] noise (higher = rarer)
)
