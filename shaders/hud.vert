#version 330 core

// Uniforms:
// Projection matrix used to convert world coordinates to screen space
uniform mat4 projection;

// Position of the object in 2D screen space
uniform vec2 position;

// Size (scale) of the object
uniform vec2 size;

// Input attributes:
// 2D vertex position of the quad (typically from -0.5 to 0.5 or 0.0 to 1.0)
layout(location = 0) in vec2 in_position;

// Texture coordinates associated with the vertex
layout(location = 1) in vec2 in_texture_coords;

// Output texture coordinates to pass to the fragment shader
out vec2 v_texture_coords;

void main() {
    // Scale and translate the vertex position based on size and position
    vec2 pos = position + in_position * size;

    // Compute final vertex position in clip space
    gl_Position = projection * vec4(pos, 0.0, 1.0);

    // Pass the texture coordinates to the fragment shader
    v_texture_coords = in_texture_coords;
}