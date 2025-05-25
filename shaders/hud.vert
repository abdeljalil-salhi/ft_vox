#version 330 core

// Vertex attribute: position of the vertex (2D)
layout (location = 0) in vec2 in_position;

// Vertex attribute: texture coordinate
layout (location = 1) in vec2 in_texture_coords;

// Passed to the fragment shader
out vec2 texture_coords;

// Projection matrix used to transform 2D coordinates to screen space
uniform mat4 projection;

// The position where the object should be drawn
uniform vec2 position;

// The size (scale) of the object
uniform vec2 size;

void main() {
    // Scale and translate the vertex position
    vec2 scaled_position = in_position * size + position;

    // Apply projection to get final screen-space position
    gl_Position = projection * vec4(scaled_position, 0.0, 1.0);

    // Pass the texture coordinate to the fragment shader
    texture_coords = in_texture_coords;
}