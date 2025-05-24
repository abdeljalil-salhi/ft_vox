from math import hypot
from random import random
from numba import njit
from numpy import ndarray

from objects.texturing import TerrainLevel, Texture
from srcs.noise import noise2, noise3
from settings import CENTER_XZ, CENTER_Y, CHUNK_AREA, CHUNK_SIZE


@njit
def get_height(x: int, z: int) -> int:
    # Island mask
    island = 1 / (pow(0.0025 * hypot(x - CENTER_XZ, z - CENTER_XZ), 20) + 0.0001)
    island = min(island, 1.0)

    # Terrain parameters
    amplitude1 = CENTER_Y
    amplitude2, amplitude4, amplitude8 = (
        amplitude1 * 0.5,
        amplitude1 * 0.25,
        amplitude1 * 0.125,
    )
    frequency1 = 0.005
    frequency2, frequency4, frequency8 = frequency1 * 2, frequency1 * 4, frequency1 * 8

    # Erosion effect
    if noise2(0.1 * x, 0.1 * z) < 0:
        amplitude1 /= 1.07

    # Terrain generation
    height = noise2(x * frequency1, z * frequency1) * amplitude1 + amplitude1
    height += noise2(x * frequency2, z * frequency2) * amplitude2 - amplitude2
    height += noise2(x * frequency4, z * frequency4) * amplitude4 + amplitude4
    height += noise2(x * frequency8, z * frequency8) * amplitude8 - amplitude8

    return int(max(height, 1) * island)


@njit
def get_index(x: int, y: int, z: int) -> int:
    return x + CHUNK_SIZE * z + CHUNK_AREA * y


@njit
def set_voxel_id(
    voxels: ndarray,
    x: int,
    y: int,
    z: int,
    wx: int,
    wy: int,
    wz: int,
    world_height: int,
) -> None:
    voxel_id = 0

    if wy < world_height - 1:
        voxel_id = Texture.STONE.value
    else:
        rng = int(7 * random())
        ry = wy - rng
        if TerrainLevel.SNOW.value <= ry < world_height:
            voxel_id = Texture.SNOW.value
        elif TerrainLevel.STONE.value <= ry < TerrainLevel.SNOW.value:
            voxel_id = Texture.STONE.value
        elif TerrainLevel.DIRT.value <= ry < TerrainLevel.STONE.value:
            voxel_id = Texture.DIRT.value
        elif TerrainLevel.GRASS.value <= ry < TerrainLevel.DIRT.value:
            voxel_id = Texture.GRASS.value
        else:
            voxel_id = Texture.SAND.value

    voxels[get_index(x, y, z)] = voxel_id
