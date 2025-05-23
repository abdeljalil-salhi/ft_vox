from typing import TYPE_CHECKING
from moderngl import Program

if TYPE_CHECKING:
    from main import Engine


class Shader:
    def __init__(self, game: "Engine") -> None:
        self.game = game
        self.context = game.context

    def update(self) -> None:
        """
        Update the shader program if needed.
        This method can be used to update uniforms or other properties of the shader.
        """
        pass

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
