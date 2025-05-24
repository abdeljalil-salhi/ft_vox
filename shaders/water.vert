#version 330 core

layout (location = 0) in vec2 in_texture_coords; // UV coordinates for the quad
layout (location = 1) in vec3 in_position;       // Vertex position (local)

uniform mat4 matrix_projection;                 // Projection matrix (perspective)
uniform mat4 matrix_view;                       // View matrix (camera)
uniform int water_area;                         // Controls water size (scaling factor)
uniform float water_line;                       // Vertical height of water surface

out vec2 uv;                                    // Pass texture coordinates to fragment shader

void main(void)
{
    vec3 position = in_position;

    // Scale and center the XZ coordinates to form a water plane
    position.xz *= water_area;                  // Scale to match desired size
    position.xz -= 0.33 * water_area;           // Offset to center the water area

    // Raise Y position to water height level
    position.y += water_line;

    // Scale UVs to tile the texture over the water plane
    uv = in_texture_coords * water_area;

    // Compute the final vertex position in clip space
    gl_Position = matrix_projection * matrix_view * vec4(position, 1.0);
}