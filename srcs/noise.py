from numba import njit
from opensimplex.internals import _init, _noise2, _noise3

from settings import SEED

perm, perm_grad_index3 = _init(seed=SEED)


@njit(cache=True)
def noise2(x: float, y: float) -> float:
    """
    Generate 2D OpenSimplex noise.
    
    Used to create the terrain heightmap.
    """
    return _noise2(x, y, perm)


@njit(cache=True)
def noise3(x, y, z):
    """
    Generate 3D OpenSimplex noise.
    
    Used to create the cave system.
    """
    return _noise3(x, y, z, perm, perm_grad_index3)
