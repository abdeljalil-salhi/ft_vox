from numba import njit, uint8
from glm import vec3
from numpy import empty, ndarray

from settings import (
    CHUNK_AREA,
    CHUNK_SIZE,
    CHUNK_VOLUME,
    WORLD_AREA,
    WORLD_DEPTH,
    WORLD_HEIGHT,
    WORLD_WIDTH,
)


@njit
def to_uint8(x: int, y: int, z: int, voxel_id: int, face_id: int) -> tuple:
    """
    Converts given attributes into 8-bit unsigned integers (used per vertex)
    """
    return uint8(x), uint8(y), uint8(z), uint8(voxel_id), uint8(face_id)


@njit
def get_chunk_index(world_voxel_position: vec3) -> int:
    """Converts world voxel position to its corresponding chunk index in the `world_voxels` array

    Args:
        world_voxel_position (vec3): 3D position of the voxel in the world

    Returns:
        int: chunk index in the `world_voxels` array
    """
    wx, wy, wz = world_voxel_position
    cx = wx // CHUNK_SIZE
    cy = wy // CHUNK_SIZE
    cz = wz // CHUNK_SIZE

    if not (0 <= cx < WORLD_WIDTH and 0 <= cy < WORLD_HEIGHT and 0 <= cz < WORLD_DEPTH):
        return -1

    return cx + WORLD_WIDTH * cz + WORLD_AREA * cy


@njit
def is_void(
    local_voxel_position: vec3, world_voxel_position: vec3, world_voxels: ndarray
) -> bool:
    """
    Checks if the voxel at the given world position is empty (or "air")

    Args:
        local_voxel_position (vec3): 3D position of the voxel in the chunk
        world_voxel_position (vec3): 3D position of the voxel in the world
        world_voxels (ndarray): 3D array of voxel data for the entire world

    Returns:
        bool: True if the voxel is empty, False otherwise
    """
    chunk_index = get_chunk_index(world_voxel_position)
    if chunk_index == -1:
        return False  # Out of bounds

    chunk_voxels = world_voxels[chunk_index]
    x, y, z = local_voxel_position

    # Check if the voxel is out of bounds
    return not chunk_voxels[
        x % CHUNK_SIZE + z % CHUNK_SIZE * CHUNK_SIZE + y % CHUNK_SIZE * CHUNK_AREA
    ]


@njit
def add_data(vertex_data: ndarray, index: int, *vertices: tuple) -> int:
    """
    Adds vertex data to the vertex_data array

    Args:
        vertex_data (ndarray): array to store vertex data
        index (int): current index in the `vertex_data` array

    Returns:
        int: updated index in the `vertex_data` array
    """
    for vertex in vertices:
        for attr in vertex:
            vertex_data[index] = attr
            index += 1
    return index


@njit
def build_chunk_mesh(
    chunk_voxels: ndarray,
    format_size: int,
    chunk_position: tuple,
    world_voxels: ndarray,
) -> ndarray:
    """
    Builds vertex data for a chunk mesh.

    Each face is made of 2 triangles (6 vertices).
    Each vertex has 5 bytes: x, y, z, voxel_id, face_id.

    Args:
        chunk_voxels (ndarray): 3D array of voxel data for the chunk
        format_size (int): size of the vertex format
        chunk_position (tuple): position of the chunk in the world
        world_voxels (ndarray): 3D array of voxel data for the entire world

    Returns:
        ndarray: vertex data for the chunk mesh
    """
    # Allocate a large enough buffer to hold the maximum number of vertices (overestimation)
    vertex_data = empty(CHUNK_VOLUME * 18 * format_size, dtype="uint8")
    index = 0

    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                voxel_id = chunk_voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y]
                if not voxel_id:
                    continue  # Skip empty voxels

                # Calculate the world position of the voxel
                cx, cy, cz = chunk_position
                wx = x + cx * CHUNK_SIZE
                wy = y + cy * CHUNK_SIZE
                wz = z + cz * CHUNK_SIZE

                # Check and add mesh data for each of the 6 faces
                # If the neighboring voxel is void (air), the face is visible

                # Top face (+y)
                if is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels):
                    v0 = to_uint8(x, y + 1, z, voxel_id, 0)
                    v1 = to_uint8(x + 1, y + 1, z, voxel_id, 0)
                    v2 = to_uint8(x + 1, y + 1, z + 1, voxel_id, 0)
                    v3 = to_uint8(x, y + 1, z + 1, voxel_id, 0)

                    index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

                # Bottom face (-y)
                if is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels):
                    v0 = to_uint8(x, y, z, voxel_id, 1)
                    v1 = to_uint8(x + 1, y, z, voxel_id, 1)
                    v2 = to_uint8(x + 1, y, z + 1, voxel_id, 1)
                    v3 = to_uint8(x, y, z + 1, voxel_id, 1)

                    index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

                # Right face (+x)
                if is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels):
                    v0 = to_uint8(x + 1, y, z, voxel_id, 2)
                    v1 = to_uint8(x + 1, y + 1, z, voxel_id, 2)
                    v2 = to_uint8(x + 1, y + 1, z + 1, voxel_id, 2)
                    v3 = to_uint8(x + 1, y, z + 1, voxel_id, 2)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # Left face (-x)
                if is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels):
                    v0 = to_uint8(x, y, z, voxel_id, 3)
                    v1 = to_uint8(x, y + 1, z, voxel_id, 3)
                    v2 = to_uint8(x, y + 1, z + 1, voxel_id, 3)
                    v3 = to_uint8(x, y, z + 1, voxel_id, 3)

                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                # Back face (-z)
                if is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels):
                    v0 = to_uint8(x, y, z, voxel_id, 4)
                    v1 = to_uint8(x, y + 1, z, voxel_id, 4)
                    v2 = to_uint8(x + 1, y + 1, z, voxel_id, 4)
                    v3 = to_uint8(x + 1, y, z, voxel_id, 4)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # Front face (+z)
                if is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels):
                    v0 = to_uint8(x, y, z + 1, voxel_id, 5)
                    v1 = to_uint8(x, y + 1, z + 1, voxel_id, 5)
                    v2 = to_uint8(x + 1, y + 1, z + 1, voxel_id, 5)
                    v3 = to_uint8(x + 1, y, z + 1, voxel_id, 5)

                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

    # Return only the portion of the vertex data array that was filled
    return vertex_data[: index + 1]
