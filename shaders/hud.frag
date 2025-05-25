#version 330 core

// Uniforms:
// Color to use when no texture is applied
uniform vec4 color;

// Boolean flag to determine whether to use a texture or flat color
uniform bool use_texture;

// Sampler for the 2D texture
uniform sampler2D tex;

// Input texture coordinates from the vertex shader
in vec2 v_texture_coords;

// Output color of the fragment (pixel)
layout(location = 0) out vec4 fragColor;

void main() {
    // If use_texture is true, sample the color from the texture using the provided coordinates
    if (use_texture) {
        fragColor = texture(tex, v_texture_coords);
    } 
    // Otherwise, use the specified uniform color
    else {
        fragColor = color;
    }
}