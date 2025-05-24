#version 330 core

layout (location = 0) in uint packed_data;

// Unpacked attributes
int x, y, z;           // Voxel position
int ao_id;             // Ambient occlusion level (0–3)
int flip_id;           // Indicates flipped face for UV mapping (0 or 1)

// Transformation matrices for rendering
uniform mat4 matrix_projection;
uniform mat4 matrix_view;
uniform mat4 matrix_model;

flat out int voxel_id; // Unique identifier for voxel type (used for hashing color)
flat out int face_id;  // Face direction index (0–5)

// Shading mode (0 = flat, 1 = directional, 2 = directional + AO)
uniform int shading_mode;

// Outputs to the fragment shader
out vec3 voxel_color;              // Final color for this voxel
out vec2 uv;                       // UV coordinate for this vertex
out float shading;                 // Shading intensity based on face direction and AO
out vec3 fragment_world_position;  // World position of the fragment for underwater effects


// Ambient Occlusion brightness levels (0 = darkest, 3 = brightest)
const float ao_values[4] = float[4](
    0.1, 0.25,
    0.5, 1.0
);

// Base shading per face direction (top, bottom, right, left, front, back)
const float face_shading[6] = float[6](
    1.0, 0.5,  // top, bottom
    0.5, 0.8,  // right, left
    0.5, 0.8   // front, back
);

// 4 UV coordinates for a quad (2 triangles per face)
const vec2 uv_coords[4] = vec2[4](
    vec2(0.0, 0.0),
    vec2(0.0, 1.0),
    vec2(1.0, 0.0),
    vec2(1.0, 1.0)
);

// Index map to assign UV coordinates per triangle and face orientation
// Handles both normal and flipped triangle winding
const int uv_indices[24] = int[24](
    1, 0, 2, 1, 2, 3, // even faces
    3, 0, 2, 3, 1, 0, // odd faces
    3, 1, 0, 3, 0, 2, // even flipped faces
    1, 2, 3, 1, 0, 2  // odd flipped faces
);

// Hashing function to generate pseudo-random but deterministic color from voxel ID
vec3 hash31(float p)
{
    vec3 p3 = fract(vec3(p * 21.2) * vec3(0.1031, 0.1030, 0.0973));
    p3 += dot(p3, p3.yzx + 33.33);
    return fract((p3.xxy + p3.yzz) * p3.zyx) + 0.05;
}

// Unpack the packed data into individual components
void unpack(uint packed_data)
{
    // Each variable (x, y, z, voxel_id, face_id, ao_id, flip_id) is packed into bits of a single uint.
    // We define the number of bits each value occupies:
    uint b_bit = 6u;  // y uses 6 bits
    uint c_bit = 6u;  // z uses 6 bits
    uint d_bit = 8u;  // voxel_id uses 8 bits
    uint e_bit = 3u;  // face_id uses 3 bits
    uint f_bit = 2u;  // ao_id (ambient occlusion) uses 2 bits
    uint g_bit = 1u;  // flip_id uses 1 bit

    // Define masks to extract only the bits we're interested in for each component
    uint b_mask = 63u;   // 0b111111 (6 bits)
    uint c_mask = 63u;   // 0b111111 (6 bits)
    uint d_mask = 255u;  // 0b11111111 (8 bits)
    uint e_mask = 7u;    // 0b111 (3 bits)
    uint f_mask = 3u;    // 0b11 (2 bits)
    uint g_mask = 1u;    // 0b1 (1 bit)

    // Calculate bit offsets for each field (from least significant bit to most)
    uint fg_bit = f_bit + g_bit;             // Total bits for ao_id + flip_id
    uint efg_bit = e_bit + fg_bit;           // Total bits for face_id + ao_id + flip_id
    uint defg_bit = d_bit + efg_bit;         // Total bits for voxel_id + face_id + ao_id + flip_id
    uint cdefg_bit = c_bit + defg_bit;       // Total bits for z + voxel_id + face_id + ao_id + flip_id
    uint bcdefg_bit = b_bit + cdefg_bit;     // Total bits for y + z + voxel_id + face_id + ao_id + flip_id

    // Unpack each variable by shifting and masking
    x = int(packed_data >> bcdefg_bit);                         // Remaining most significant bits for x
    y = int((packed_data >> cdefg_bit) & b_mask);               // Next 6 bits for y
    z = int((packed_data >> defg_bit) & c_mask);                // Next 6 bits for z
    voxel_id = int((packed_data >> efg_bit) & d_mask);          // Next 8 bits for voxel_id
    face_id = int((packed_data >> fg_bit) & e_mask);            // Next 3 bits for face_id
    ao_id = int((packed_data >> g_bit) & f_mask);               // Next 2 bits for ao_id
    flip_id = int(packed_data & g_mask);                        // Last 1 bit for flip_id
}

void main()
{
    // Decode packed data
    unpack(packed_data);

    // Construct the 3D position of this vertex
    vec3 in_position = vec3(x, y, z);

    // Compute UV index:
    // - `gl_VertexID % 6`: gives the current vertex within a quad (0–5)
    // - `(face_id & 1)`: even/odd face
    // - `flip_id`: flipped triangle winding
    // Result: offset into `uv_indices` for correct UV assignment
    int uv_index = gl_VertexID % 6 + ((face_id & 1) + flip_id * 2) * 6;

    // Get UV coordinate from lookup table
    uv = uv_coords[uv_indices[uv_index]];

    // Determine voxel color using hashed voxel_id
    voxel_color = hash31(voxel_id);

    // Determine shading based on selected mode
    if (shading_mode == 0)
        shading = 1.0;  // Flat shading
    else if (shading_mode == 1)
        shading = face_shading[face_id];  // Directional lighting
    else if (shading_mode == 2)
        shading = face_shading[face_id] * ao_values[ao_id];  // Directional + AO
    
    // Set fragment world position
    // This is the position in world space, used for effects like underwater rendering
    fragment_world_position = (matrix_model * vec4(in_position, 1.0)).xyz;

    // Final position in clip space
    gl_Position = matrix_projection * matrix_view * vec4(fragment_world_position, 1.0);
}