#version 330 core

// Input attributes:
// Vertex position in object space
layout (location = 0) in vec3 in_position;
// Per-vertex color
layout (location = 1) in vec3 in_color;

// Transformation matrices (typically set from the CPU side)
uniform mat4 matrix_projection;  // Projection matrix (e.g. perspective)
uniform mat4 matrix_view;        // View matrix (camera)
uniform mat4 matrix_model;       // Model matrix (object transform)

// Output to the fragment shader
out vec3 color;

void main(void)
{
    // Pass the vertex color directly to the fragment shader
    color = in_color;

    // Transform the vertex position to clip space
    gl_Position = matrix_projection * matrix_view * matrix_model * vec4(in_position, 1.0);
}