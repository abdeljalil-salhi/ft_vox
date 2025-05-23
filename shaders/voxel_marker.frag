#version 330 core

// Output color of the fragment (pixel)
layout (location = 0) out vec4 fragColor;

// Input from the vertex shader: the color to tint the marker with
in vec3 marker_color;

// UV coordinates for texture sampling
in vec2 uv;

// Texture sampler
uniform sampler2D unit_texture;

void main(void)
{
    // Sample the texture at the given UV coordinates
    fragColor = texture(unit_texture, uv);

    // Add the marker's color tint to the sampled texture color
    fragColor.rgb += marker_color;

    // Conditionally set the alpha (transparency):
    // If red + blue > 1.0, make it fully transparent (alpha = 0.0)
    // Otherwise, keep it fully opaque (alpha = 1.0)
    fragColor.a = (fragColor.r + fragColor.b > 1.0) ? 0.0 : 1.0;
}