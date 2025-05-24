from typing import TYPE_CHECKING
from glm import mat4
from moderngl import Program

from objects.texturing import CLOUD_SCALE, SKYBOX_COLOR, WATER_AREA, WATER_LINE
from settings import CENTER_XZ

if TYPE_CHECKING:
    from srcs.engine import Engine


class Shader:
    def __init__(self, game: "Engine") -> None:
        self.game = game
        self.context = game.context
        self.player = game.player
        self.chunk = self.get_program("chunk")
        self.voxel_marker = self.get_program("voxel_marker")
        self.water = self.get_program("water")
        self.clouds = self.get_program("clouds")

        self.set_uniforms_on_init()

    def set_uniforms_on_init(self) -> None:
        self.chunk["matrix_projection"].write(self.player.matrix_projection)
        self.chunk["matrix_model"].write(mat4())
        self.chunk["skybox_color"].write(SKYBOX_COLOR)
        self.chunk["water_line"] = WATER_LINE
        self.chunk["unit_no_texture"] = 0
        self.chunk["unit_texture_array"] = 1

        self.voxel_marker["matrix_projection"].write(self.player.matrix_projection)
        self.voxel_marker["matrix_model"].write(mat4())
        self.voxel_marker["unit_texture"] = 0

        self.water["matrix_projection"].write(self.player.matrix_projection)
        self.water["unit_texture"] = 2
        self.water["water_area"] = WATER_AREA
        self.water["water_line"] = WATER_LINE

        self.clouds["matrix_projection"].write(self.player.matrix_projection)
        self.clouds["center"] = CENTER_XZ
        self.clouds["skybox_color"].write(SKYBOX_COLOR)
        self.clouds["cloud_scale"] = CLOUD_SCALE

    def update(self) -> None:
        """
        Update the shader program if needed.
        This method can be used to update uniforms or other properties of the shader.
        """
        self.chunk["matrix_view"].write(self.player.matrix_view)
        self.voxel_marker["matrix_view"].write(self.player.matrix_view)
        self.water["matrix_view"].write(self.player.matrix_view)
        self.clouds["matrix_view"].write(self.player.matrix_view)

    def get_program(self, shader_name: str) -> Program:
        """
        Loads and compiles a shader program using a vertex and fragment shader
        stored in the `shaders/` directory. Returns a ModernGL Program object.

        Args:
            shader_name (str): The name of the shader file without extension.
                               For example, 'default' would load:
                               - shaders/default.vert
                               - shaders/default.frag

        Returns:
            Program: A compiled shader program ready to be used in rendering.
        """

        with open(f"shaders/{shader_name}.vert", "r") as f:
            vertex_shader = f.read()

        with open(f"shaders/{shader_name}.frag", "r") as f:
            fragment_shader = f.read()

        return self.context.program(
            vertex_shader=vertex_shader, fragment_shader=fragment_shader
        )
