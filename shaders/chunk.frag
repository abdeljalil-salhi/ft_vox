#version 330 core

// Output color of the fragment
layout(location = 0) out vec4 fragColor;

// Gamma correction constants
const vec3 gamma = vec3(2.2);          // Standard gamma correction value
const vec3 inv_gamma = 1.0 / gamma;    // Inverse for linear-to-sRGB conversion

// Texture sampler for blank voxel
uniform sampler2D unit_no_texture;
// Texture sampler for texture array
uniform sampler2DArray unit_texture_array;
// Skybox color for fog effect
uniform vec3 skybox_color;

// Flag to enable/disable texture mapping
uniform bool textures_enabled;

// Interpolated values from the vertex shader
in vec3 voxel_color;   // Color derived from voxel_id hashing
in vec2 uv;            // UV coordinates for sampling the texture
in float shading;      // Shading intensity based on face and AO

// Interpolated values from the geometry shader
flat in int voxel_id;  // Unique identifier for voxel type (used for hashing color)
flat in int face_id;   // Face direction index (0–5)

void main()
{
    vec2 face_uv = uv;
    face_uv.x = uv.x / 3.0 - min(face_id, 2) / 3.0;

    vec3 texture_color = vec3(0.0);

    if (textures_enabled)
    {
        // Sample from the texture array using the voxel_id and face_uv
        texture_color = texture(unit_texture_array, vec3(face_uv, voxel_id)).rgb;

        // Apply gamma correction (sRGB to linear space)
        texture_color = pow(texture_color, gamma);
    }
    else
    {
        // Sample base color from the texture using interpolated UVs
        texture_color = texture(unit_no_texture, uv).rgb;

        // Apply gamma correction (sRGB to linear space)
        texture_color = pow(texture_color, gamma);

        // Modulate with the voxel-specific color
        texture_color.rgb *= voxel_color;
    }

    // Apply final shading (includes directional and/or AO)
    texture_color *= shading;

    // Apply fog effect based on distance from camera
    float fog_distance = gl_FragCoord.z / gl_FragCoord.w;
    texture_color = mix(texture_color, skybox_color, (1.0 - exp2(-0.00001 * fog_distance * fog_distance)));

    // Convert back to sRGB space (linear to sRGB)
    texture_color = pow(texture_color, inv_gamma);

    // Output final color with full alpha
    fragColor = vec4(texture_color, 1.0);
}