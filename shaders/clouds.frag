#version 330 core

// Output color of the pixel
layout (location = 0) out vec4 fragColor;

// Constant white cloud color
const vec3 cloud_color = vec3(1);  // RGB = (1,1,1) => white

// Skybox color (background color)
uniform vec3 skybox_color;

void main(void)
{
    // Estimate distance from camera to the fragment using depth
    float fog_distance = gl_FragCoord.z / gl_FragCoord.w;

    // Blend cloud color with skybox color based on distance (fog effect)
    // The further the cloud, the more it blends with the sky
    vec3 color = mix(
        cloud_color,
        skybox_color,
        1.0 - exp(-0.000001 * fog_distance * fog_distance)
    );

    // Set the final fragment color with a constant alpha (transparency = 0.8)
    fragColor = vec4(color, 0.8);
}