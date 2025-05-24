from math import hypot
from random import random
from numba import njit

from srcs.noise import noise2, noise3
from settings import CENTER_XZ, CENTER_Y


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
