from numpy import array
from moderngl import VertexArray


class BaseMesh:
    def __init__(self) -> None:
        self.context = None
        self.shader = None
        self.vbo_format = (
            None  # e.g. "3f 3f" for 3 floats for position and 3 floats for color
        )
        self.attrs: tuple[str, ...] = None  # e.g. ("in_position", "in_color")
        self.vao = None

    # This method is expected to be overridden by subclasses to return the mesh's vertex data
    def get_vertex_data(self) -> array: ...

    def get_vao(self) -> VertexArray:
        """
        Creates and returns a Vertex Array Object (VAO) for rendering the mesh.
        This binds the vertex buffer to the appropriate shader attributes.
        """
        # Get the mesh's vertex data (defined in subclass)
        vertex_data = self.get_vertex_data()
        # Create a Vertex Buffer Object (VBO) from the vertex data
        vbo = self.context.buffer(vertex_data)
        # Create and return the VAO, which links the VBO to the shader inputs
        return self.context.vertex_array(
            self.shader,  # shader program to use
            [(vbo, self.vbo_format, *self.attrs)],  # VBO format and attribute mapping
            skip_errors=True,  # skip errors if attributes don't match exactly
        )

    def render(self) -> None:
        """
        Renders the mesh by issuing a draw call using its VAO.
        IMPORTANT: Assumes `self.vao` has already been created and set up.
        """
        self.vao.render()
