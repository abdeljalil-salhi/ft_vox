from typing import TYPE_CHECKING
from glm import mat4
from moderngl import Program

if TYPE_CHECKING:
    from srcs.engine import Engine


class Shader:
    def __init__(self, game: "Engine") -> None:
        self.game = game
        self.context = game.context
        self.player = game.player
        self.chunk = self.get_program("chunk")
        self.voxel_marker = self.get_program("voxel_marker")

        self.set_uniforms_on_init()

    def set_uniforms_on_init(self) -> None:
        self.chunk["matrix_projection"].write(self.player.matrix_projection)
        self.chunk["matrix_model"].write(mat4())
        self.chunk["unit_texture_0"] = 0

        self.voxel_marker["matrix_projection"].write(self.player.matrix_projection)
        self.voxel_marker["matrix_model"].write(mat4())
        self.voxel_marker["unit_texture"] = 0

    def update(self) -> None:
        """
        Update the shader program if needed.
        This method can be used to update uniforms or other properties of the shader.
        """
        self.chunk["matrix_view"].write(self.player.matrix_view)
        self.voxel_marker["matrix_view"].write(self.player.matrix_view)

    def get_program(self, shader_name: str) -> Program:
        """
        Loads and compiles a shader program using a vertex and fragment shader
        stored in the 'shaders/' directory. Returns a ModernGL Program object.

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
