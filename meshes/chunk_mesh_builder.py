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
def get_ao(
    local_position: vec3, world_position: vec3, world_voxels: ndarray, plane: str
) -> tuple:
    """
    Calculates the ambient occlusion (AO) values for a voxel based on its local and world positions.

    NOTE:
    This function samples the 8 surrounding voxels of a face based on its plane ("X", "Y", or "Z"),
    checks if each neighbor is empty (is_void), and then groups them into four sets of three.
    Each group corresponds to one corner of the face and is used to determine the level of AO to apply for shading.

    Args:
        local_position (vec3): 3D position of the voxel in the chunk
        world_position (vec3): 3D position of the voxel in the world
        world_voxels (ndarray): 3D array of voxel data for the entire world
        plane (str): The plane of the face ("X", "Y", or "Z")

    Returns:
        tuple: Four values representing the ambient occlusion for each corner of the face.
    """
    x, y, z = local_position
    wx, wy, wz = world_position

    # Determine which set of adjacent voxels to check based on the face's orientation (plane)
    if plane == "Y":
        # AO on horizontal (top/bottom) face — we scan around the XZ plane
        a = is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels)  # Behind
        b = is_void((x - 1, y, z - 1), (wx - 1, wy, wz - 1), world_voxels)  # Back-left
        c = is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels)  # Left
        d = is_void((x - 1, y, z + 1), (wx - 1, wy, wz + 1), world_voxels)  # Front-left
        e = is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels)  # Front
        f = is_void(
            (x + 1, y, z + 1), (wx + 1, wy, wz + 1), world_voxels
        )  # Front-right
        g = is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels)  # Right
        h = is_void((x + 1, y, z - 1), (wx + 1, wy, wz - 1), world_voxels)  # Back-right

    elif plane == "X":
        # AO on vertical X face — we scan around the YZ plane
        a = is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels)  # Behind
        b = is_void(
            (x, y - 1, z - 1), (wx, wy - 1, wz - 1), world_voxels
        )  # Bottom-back
        c = is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels)  # Bottom
        d = is_void(
            (x, y - 1, z + 1), (wx, wy - 1, wz + 1), world_voxels
        )  # Bottom-front
        e = is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels)  # Front
        f = is_void((x, y + 1, z + 1), (wx, wy + 1, wz + 1), world_voxels)  # Top-front
        g = is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels)  # Top
        h = is_void((x, y + 1, z - 1), (wx, wy + 1, wz - 1), world_voxels)  # Top-back

    elif plane == "Z":
        # AO on vertical Z face — we scan around the XY plane
        a = is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels)  # Left
        b = is_void(
            (x - 1, y - 1, z), (wx - 1, wy - 1, wz), world_voxels
        )  # Bottom-left
        c = is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels)  # Bottom
        d = is_void(
            (x + 1, y - 1, z), (wx + 1, wy - 1, wz), world_voxels
        )  # Bottom-right
        e = is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels)  # Right
        f = is_void((x + 1, y + 1, z), (wx + 1, wy + 1, wz), world_voxels)  # Top-right
        g = is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels)  # Top
        h = is_void((x - 1, y + 1, z), (wx - 1, wy + 1, wz), world_voxels)  # Top-left

    # FINALLY we have how much ambient occlusion should be applied
    return (a + b + c), (g + h + a), (e + f + g), (c + d + e)


@njit
def to_uint8(x: int, y: int, z: int, voxel_id: int, face_id: int, ao_id: int) -> tuple:
    """
    Converts given attributes into 8-bit unsigned integers (used per vertex)
    """
    return uint8(x), uint8(y), uint8(z), uint8(voxel_id), uint8(face_id), uint8(ao_id)


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

                # To solve the problem of AO being higher on the opposite side,
                # we flip the face if the AO is higher on the opposite side

                # Top face (+y)
                if is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels):
                    ao = get_ao((x, y + 1, z), (wx, wy + 1, wz), world_voxels, "Y")
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = to_uint8(x, y + 1, z, voxel_id, 0, ao[0])
                    v1 = to_uint8(x + 1, y + 1, z, voxel_id, 0, ao[1])
                    v2 = to_uint8(x + 1, y + 1, z + 1, voxel_id, 0, ao[2])
                    v3 = to_uint8(x, y + 1, z + 1, voxel_id, 0, ao[3])

                    if flip_id:
                        index = add_data(vertex_data, index, v1, v0, v3, v1, v3, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

                # Bottom face (-y)
                if is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels):
                    ao = get_ao((x, y - 1, z), (wx, wy - 1, wz), world_voxels, "Y")
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = to_uint8(x, y, z, voxel_id, 1, ao[0])
                    v1 = to_uint8(x + 1, y, z, voxel_id, 1, ao[1])
                    v2 = to_uint8(x + 1, y, z + 1, voxel_id, 1, ao[2])
                    v3 = to_uint8(x, y, z + 1, voxel_id, 1, ao[3])

                    if flip_id:
                        index = add_data(vertex_data, index, v1, v3, v0, v1, v2, v3)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

                # Right face (+x)
                if is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels):
                    ao = get_ao((x + 1, y, z), (wx + 1, wy, wz), world_voxels, "X")
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = to_uint8(x + 1, y, z, voxel_id, 2, ao[0])
                    v1 = to_uint8(x + 1, y + 1, z, voxel_id, 2, ao[1])
                    v2 = to_uint8(x + 1, y + 1, z + 1, voxel_id, 2, ao[2])
                    v3 = to_uint8(x + 1, y, z + 1, voxel_id, 2, ao[3])

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # Left face (-x)
                if is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels):
                    ao = get_ao((x - 1, y, z), (wx - 1, wy, wz), world_voxels, "X")
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = to_uint8(x, y, z, voxel_id, 3, ao[0])
                    v1 = to_uint8(x, y + 1, z, voxel_id, 3, ao[1])
                    v2 = to_uint8(x, y + 1, z + 1, voxel_id, 3, ao[2])
                    v3 = to_uint8(x, y, z + 1, voxel_id, 3, ao[3])

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v1, v0, v3, v2, v1)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                # Back face (-z)
                if is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels):
                    ao = get_ao((x, y, z - 1), (wx, wy, wz - 1), world_voxels, "Z")
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = to_uint8(x, y, z, voxel_id, 4, ao[0])
                    v1 = to_uint8(x, y + 1, z, voxel_id, 4, ao[1])
                    v2 = to_uint8(x + 1, y + 1, z, voxel_id, 4, ao[2])
                    v3 = to_uint8(x + 1, y, z, voxel_id, 4, ao[3])

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # Front face (+z)
                if is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels):
                    ao = get_ao((x, y, z + 1), (wx, wy, wz + 1), world_voxels, "Z")
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = to_uint8(x, y, z + 1, voxel_id, 5, ao[0])
                    v1 = to_uint8(x, y + 1, z + 1, voxel_id, 5, ao[1])
                    v2 = to_uint8(x + 1, y + 1, z + 1, voxel_id, 5, ao[2])
                    v3 = to_uint8(x + 1, y, z + 1, voxel_id, 5, ao[3])

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v1, v0, v3, v2, v1)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

    # Return only the portion of the vertex data array that was filled
    return vertex_data[: index + 1]
