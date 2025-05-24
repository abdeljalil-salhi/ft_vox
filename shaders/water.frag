#version 330 core

layout (location = 0) out vec4 fragColor; // Final output color

const vec3 gamma = vec3(2.2);            // Gamma correction factor
const vec3 inv_gamma = 1 / gamma;        // Inverse gamma for final correction

in vec2 uv;                              // Interpolated texture coordinates from vertex shader

uniform sampler2D unit_texture;         // Water texture

void main(void)
{
    // Sample the texture color at the current UV coordinate
    vec3 texture_color = texture(unit_texture, uv).rgb;

    // Apply gamma correction to linearize the texture color
    texture_color = pow(texture_color, gamma);

    // Compute the distance from the camera using perspective depth
    float fog_distance = gl_FragCoord.z / gl_FragCoord.w;

    // Compute the fog alpha based on exponential falloff
    float alpha = mix(0.5, 0.0, 1.0 - exp(-0.000002 * fog_distance * fog_distance));

    // Apply inverse gamma correction to return to sRGB space
    texture_color = pow(texture_color, inv_gamma);

    // Output the final color with computed alpha (transparency)
    fragColor = vec4(texture_color, alpha);
}