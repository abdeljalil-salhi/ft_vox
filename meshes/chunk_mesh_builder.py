from glm import vec3
from numpy import empty, ndarray

from settings import CHUNK_AREA, CHUNK_SIZE, CHUNK_VOLUME


def is_void(voxel_position: vec3, chunk_voxels: ndarray) -> bool:
    """
    Check if the voxel at the given position is void (empty).
    """
    x, y, z = voxel_position
    if 0 <= x < CHUNK_SIZE and 0 <= y < CHUNK_SIZE and 0 <= z < CHUNK_SIZE:
        if chunk_voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y]:
            return False
    return True


def add_data(vertex_data: ndarray, index: int, *vertices: tuple) -> int:
    for vertex in vertices:
        for attr in vertex:
            vertex_data[index] = attr
            index += 1
    return index


def build_chunk_mesh(chunk_voxels: ndarray, format_size: int) -> ndarray:
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

                # Top face
                if is_void((x, y + 1, z), chunk_voxels):
                    v0 = (x, y + 1, z, voxel_id, 0)
                    v1 = (x + 1, y + 1, z, voxel_id, 0)
                    v2 = (x + 1, y + 1, z + 1, voxel_id, 0)
                    v3 = (x, y + 1, z + 1, voxel_id, 0)

                    index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

                # Bottom face
                if is_void((x, y - 1, z), chunk_voxels):
                    v0 = (x, y, z, voxel_id, 1)
                    v1 = (x + 1, y, z, voxel_id, 1)
                    v2 = (x + 1, y, z + 1, voxel_id, 1)
                    v3 = (x, y, z + 1, voxel_id, 1)

                    index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

                # Right face
                if is_void((x + 1, y, z), chunk_voxels):
                    v0 = (x + 1, y, z, voxel_id, 2)
                    v1 = (x + 1, y + 1, z, voxel_id, 2)
                    v2 = (x + 1, y + 1, z + 1, voxel_id, 2)
                    v3 = (x + 1, y, z + 1, voxel_id, 2)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # Left face
                if is_void((x - 1, y, z), chunk_voxels):
                    v0 = (x, y, z, voxel_id, 3)
                    v1 = (x, y + 1, z, voxel_id, 3)
                    v2 = (x, y + 1, z + 1, voxel_id, 3)
                    v3 = (x, y, z + 1, voxel_id, 3)

                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                # Back face
                if is_void((x, y, z - 1), chunk_voxels):
                    v0 = (x, y, z, voxel_id, 4)
                    v1 = (x, y + 1, z, voxel_id, 4)
                    v2 = (x + 1, y + 1, z, voxel_id, 4)
                    v3 = (x + 1, y, z, voxel_id, 4)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # Front face
                if is_void((x, y, z + 1), chunk_voxels):
                    v0 = (x, y, z + 1, voxel_id, 5)
                    v1 = (x, y + 1, z + 1, voxel_id, 5)
                    v2 = (x + 1, y + 1, z + 1, voxel_id, 5)
                    v3 = (x + 1, y, z + 1, voxel_id, 5)

                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

    # Only keep the used part of the vertex_data array
    return vertex_data[: index + 1]
