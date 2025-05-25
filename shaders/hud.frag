#version 330 core

// Input texture coordinates passed from the vertex shader
in vec2 texture_coords;

// Final fragment color output
out vec4 FragColor;

// Whether to use a texture or just a solid color
uniform bool use_texture;

// Texture array containing multiple layers (e.g., different block textures)
uniform sampler2DArray tex;

// The texture layer to sample from
uniform int layer;

// Fallback color used when not using texture
uniform vec4 color;

void main() {
    // If texture usage is enabled, sample the texture from the specified layer
    if (use_texture) {
        FragColor = texture(tex, vec3(texture_coords, layer));
    }
    // Otherwise, use the solid color
    else {
        FragColor = color;
    }
}