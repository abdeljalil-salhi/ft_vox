#version 330 core

// Input layout locations:
// Vertex attributes passed from the vertex buffer
layout (location = 0) in vec2 in_texture_coords; // 2D texture coordinates
layout (location = 1) in vec3 in_position;       // 3D vertex position

// Uniforms: global variables set from the CPU side (your application)
uniform mat4 matrix_projection;  // Projection matrix (e.g., perspective)
uniform mat4 matrix_view;        // View matrix (camera transformation)
uniform mat4 matrix_model;       // Model matrix (object transformation)
uniform uint mode_id;            // Marker mode ID, used to pick a color (0 or 1)

// Marker colors array: red for mode 0, blue for mode 1
const vec3 marker_colors[2] = vec3[2](
    vec3(1, 0, 0),  // Red
    vec3(0, 0, 1)   // Blue
);

// Outputs to the fragment shader
out vec3 marker_color; // Chosen marker color (based on mode)
out vec2 uv;           // Pass UV to fragment shader for texture lookup

void main(void)
{
    // Pass texture coordinates to fragment shader
    uv = in_texture_coords;

    // Select marker color based on mode_id (0 or 1)
    marker_color = marker_colors[mode_id];
    
    // Slightly inflate the marker's position to avoid z-fighting
    // (push geometry slightly outward by scaling around center)
    gl_Position = matrix_projection * matrix_view * matrix_model *
                  vec4((in_position - 0.5) * 1.01 + 0.5, 1.0);
}