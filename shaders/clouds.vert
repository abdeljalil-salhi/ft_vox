#version 330 core

// Input vertex position from the vertex buffer
layout (location = 0) in vec3 in_position;

// Uniforms (passed in from the CPU side)
uniform mat4 matrix_projection;        // Projection matrix (camera lens)
uniform mat4 matrix_view;              // View matrix (camera position and rotation)
uniform int center;                    // Center of cloud movement (usually the world center)
uniform float unit_time;               // Game time, used to animate clouds
uniform float cloud_scale;             // Scale factor for cloud size/spacing

void main(void)
{
    vec3 position = vec3(in_position);

    // Scale the XZ plane of the cloud position around the center
    // This controls the size and spacing of clouds
    position.xz -= center;         // Move to origin
    position.xz *= cloud_scale;    // Scale
    position.xz += center;         // Move back to original center

    // Animate cloud position to simulate drifting over time
    float time = 300 * sin(0.01 * unit_time);  // Oscillate position with time
    position.xz += time;                       // Offset position based on time

    // Final position in clip space (applies camera projection)
    gl_Position = matrix_projection * matrix_view * vec4(position, 1.0);
}