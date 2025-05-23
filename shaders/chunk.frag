#version 330 core

// Output color of the fragment
layout(location = 0) out vec4 fragColor;

// Gamma correction constants
const vec3 gamma = vec3(2.2);          // Standard gamma correction value
const vec3 inv_gamma = 1.0 / gamma;    // Inverse for linear-to-sRGB conversion

// Texture sampler (used for voxel face detail)
uniform sampler2D unit_texture_0;

// Interpolated values from the vertex shader
in vec3 voxel_color;   // Color derived from voxel_id hashing
in vec2 uv;            // UV coordinates for sampling the texture
in float shading;      // Shading intensity based on face and AO

void main()
{
    // Sample base color from the texture using interpolated UVs
    vec3 texture_color = texture(unit_texture_0, uv).rgb;

    // Apply gamma correction (sRGB to linear space)
    texture_color = pow(texture_color, gamma);

    // Modulate with the voxel-specific color
    texture_color.rgb *= voxel_color;

    // Convert back to sRGB space (linear to sRGB)
    texture_color = pow(texture_color, inv_gamma);

    // Apply final shading (includes directional and/or AO)
    texture_color *= shading;

    // Output final color with full alpha
    fragColor = vec4(texture_color, 1.0);
}