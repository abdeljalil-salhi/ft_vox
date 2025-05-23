#version 330 core

// Output color of the fragment (pixel)
layout (location = 0) out vec4 fragColor;

// Input color interpolated from the vertex shader
in vec3 color;

void main(void)
{
    // Set the output fragment color using the input color,
    // with an alpha value of 1.0 (fully opaque)
    fragColor = vec4(color, 1.0);
}