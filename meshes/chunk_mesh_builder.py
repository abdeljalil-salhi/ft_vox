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


def get_chunk_index(world_voxel_position: vec3) -> int:
    wx, wy, wz = world_voxel_position
    cx = wx // CHUNK_SIZE
    cy = wy // CHUNK_SIZE
    cz = wz // CHUNK_SIZE

    if not (0 <= cx < WORLD_WIDTH and 0 <= cy < WORLD_HEIGHT and 0 <= cz < WORLD_DEPTH):
        return -1

    return cx + WORLD_WIDTH * cz + WORLD_AREA * cy


def is_void(
    local_voxel_position: vec3, world_voxel_position: vec3, world_voxels: ndarray
) -> bool:
    chunk_index = get_chunk_index(world_voxel_position)
    if chunk_index == -1:
        return False

    chunk_voxels = world_voxels[chunk_index]
    x, y, z = local_voxel_position

    return not chunk_voxels[
        x % CHUNK_SIZE + z % CHUNK_SIZE * CHUNK_SIZE + y % CHUNK_SIZE * CHUNK_AREA
    ]


def add_data(vertex_data: ndarray, index: int, *vertices: tuple) -> int:
    for vertex in vertices:
        for attr in vertex:
            vertex_data[index] = attr
            index += 1
    return index


def build_chunk_mesh(
    chunk_voxels: ndarray,
    format_size: int,
    chunk_position: tuple,
    world_voxels: ndarray,
) -> ndarray:
    """
    NOTES:
    - Each vertex is represented by 5 bytes:
        - 3 bytes for the position (x, y, z)
        - 2 bytes for the texture coordinates (u, v)
    - Eeach vertex attribute is represented by 1 byte in GPU memory.
    """
    vertex_data = empty(CHUNK_VOLUME * 18 * format_size, dtype="uint8")
    index = 0

    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                voxel_id = chunk_voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y]
                if not voxel_id:
                    continue  # Skip empty voxels

                cx, cy, cz = chunk_position
                wx = x + cx * CHUNK_SIZE
                wy = y + cy * CHUNK_SIZE
                wz = z + cz * CHUNK_SIZE

                # Top face
                if is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels):
                    v0 = (x, y + 1, z, voxel_id, 0)
                    v1 = (x + 1, y + 1, z, voxel_id, 0)
                    v2 = (x + 1, y + 1, z + 1, voxel_id, 0)
                    v3 = (x, y + 1, z + 1, voxel_id, 0)

                    index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

                # Bottom face
                if is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels):
                    v0 = (x, y, z, voxel_id, 1)
                    v1 = (x + 1, y, z, voxel_id, 1)
                    v2 = (x + 1, y, z + 1, voxel_id, 1)
                    v3 = (x, y, z + 1, voxel_id, 1)

                    index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

                # Right face
                if is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels):
                    v0 = (x + 1, y, z, voxel_id, 2)
                    v1 = (x + 1, y + 1, z, voxel_id, 2)
                    v2 = (x + 1, y + 1, z + 1, voxel_id, 2)
                    v3 = (x + 1, y, z + 1, voxel_id, 2)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # Left face
                if is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels):
                    v0 = (x, y, z, voxel_id, 3)
                    v1 = (x, y + 1, z, voxel_id, 3)
                    v2 = (x, y + 1, z + 1, voxel_id, 3)
                    v3 = (x, y, z + 1, voxel_id, 3)

                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                # Back face
                if is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels):
                    v0 = (x, y, z, voxel_id, 4)
                    v1 = (x, y + 1, z, voxel_id, 4)
                    v2 = (x + 1, y + 1, z, voxel_id, 4)
                    v3 = (x + 1, y, z, voxel_id, 4)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # Front face
                if is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels):
                    v0 = (x, y, z + 1, voxel_id, 5)
                    v1 = (x, y + 1, z + 1, voxel_id, 5)
                    v2 = (x + 1, y + 1, z + 1, voxel_id, 5)
                    v3 = (x + 1, y, z + 1, voxel_id, 5)

                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

    # Only keep the used part of the vertex_data array
    return vertex_data[: index + 1]
