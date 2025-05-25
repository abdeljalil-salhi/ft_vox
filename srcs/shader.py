from typing import TYPE_CHECKING
from glm import mat4, ortho, vec4, translate, scale, rotate, vec3
from moderngl import TRIANGLE_FAN, Program, VertexArray
from numpy import array

from objects.texturing import CLOUD_SCALE, SKYBOX_COLOR, WATER_AREA, WATER_LINE
from settings import CENTER_XZ

if TYPE_CHECKING:
    from srcs.engine import Engine
    from meshes.hud_item_mesh import HUDItemMesh


class Shader:
    def __init__(self, game: "Engine") -> None:
        self.game = game
        self.context = game.context
        self.player = game.player
        self.chunk = self.get_program("chunk")
        self.voxel_marker = self.get_program("voxel_marker")
        self.water = self.get_program("water")
        self.clouds = self.get_program("clouds")
        self.hud = self.get_program("hud")

        self.quad_vao = self.create_quad_vao()
        w, h = self.game.get_window_resolution()
        self.ortho_projection = ortho(0, w, 0, h, -1, 1)

        self.set_uniforms_on_init()

    def create_quad_vao(self) -> VertexArray:
        """
        Creates a vertex array object (VAO) for rendering a 2D quad in the HUD.
        The quad is defined in normalized device coordinates (NDC) with vertices
        ranging from (0, 0) to (1, 1) for both position and texture coordinates.

        Returns:
            VertexArray: A ModernGL VertexArray object for the quad.
        """
        vertices = array(
            [
                0.0,
                0.0,
                0.0,
                0.0,  # Bottom-left
                1.0,
                0.0,
                1.0,
                0.0,  # Bottom-right
                1.0,
                1.0,
                1.0,
                1.0,  # Top-right
                0.0,
                1.0,
                0.0,
                1.0,  # Top-left
            ],
            dtype="f4",
        )
        vbo = self.context.buffer(vertices)
        vao = self.context.vertex_array(self.hud, [(vbo, "2f 2f", "in_position", "in_texture_coords")])
        return vao

    def render_2d_quad(
        self, x: float, y: float, w: float, h: float, color: vec4 = None
    ) -> None:
        """
        Renders a 2D quad in the HUD at the specified position with the given size and color.

        Args:
            x (float): X position in screen space
            y (float): Y position in screen space
            w (float): Width of the quad
            h (float): Height of the quad
            color (vec4, optional): Color of the quad. Defaults to white if None.
        """
        self.hud["projection"].write(self.ortho_projection)
        self.hud["position"].write(array([x, y], dtype="f4"))
        self.hud["size"].write(array([w, h], dtype="f4"))
        self.hud["use_texture"].value = 0
        self.hud["color"].write(color if color is not None else vec4(1.0))
        self.quad_vao.render(mode=TRIANGLE_FAN)

    def render_3d_item(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        voxel_id: int,
        hud_item_mesh: "HUDItemMesh",
    ) -> None:
        """
        Renders a 3D cube in the HUD at the specified 2D position with the given voxel texture.

        Args:
            x (float): X position in screen space
            y (float): Y position in screen space
            w (float): Width of the slot
            h (float): Height of the slot
            voxel_id (int): ID of the voxel to determine the texture layer
            hud_item_mesh (HUDItemMesh): The HUDItemMesh instance to render
        """
        # Use the chunk shader for rendering the 3D item
        shader = self.chunk

        # Save the current state of the chunk shader uniforms
        saved_projection = shader["matrix_projection"].read()
        saved_view = shader["matrix_view"].read()
        saved_model = shader["matrix_model"].read()
        saved_shading_mode = shader["shading_mode"].value
        saved_textures_enabled = shader["textures_enabled"].value
        saved_skybox_color = shader["skybox_color"].read()
        saved_water_line = shader["water_line"].value

        # Set up uniforms for the chunk shader
        shader["unit_no_texture"] = 0
        shader["unit_texture_array"] = 1
        self.game.textures.texture_array.use(location=1)
        shader["textures_enabled"].value = True
        shader["shading_mode"].value = 1  # Use directional shading for a 3D effect
        shader["skybox_color"].write(SKYBOX_COLOR)
        shader["water_line"] = WATER_LINE

        # Create a model matrix to position and scale the cube
        model = mat4(1.0)
        # Translate to center of the slot
        model = translate(model, vec3(x + w / 2, y + h / 2, 0))
        # Scale to fit within the slot (slightly smaller than the slot size)
        scale_factor = min(w, h) * 0.8  # 80% of the slot size
        model = scale(model, vec3(scale_factor, scale_factor, scale_factor))
        # Apply a slight rotation for 3D effect
        model = rotate(model, 0.5, vec3(1, 0, 0))  # Rotate around X-axis
        model = rotate(model, 0.8, vec3(0, 1, 0))  # Rotate around Y-axis
        # Center the cube (since vertices are 0 to 1)
        model = translate(model, vec3(-0.5, -0.5, -0.5))

        # Set up an orthographic projection for HUD rendering
        w, h = self.game.get_window_resolution()
        proj = ortho(0, w, 0, h, -1000, 1000)
        # Use a simple view matrix (looking straight down the Z-axis)
        view = mat4(1.0)

        # Update shader uniforms
        shader["matrix_projection"].write(proj)
        shader["matrix_view"].write(view)
        shader["matrix_model"].write(model)

        # Set the voxel_id in the mesh before rendering
        hud_item_mesh.voxel_id = voxel_id  # Use raw voxel_id, let pack_data handle it
        hud_item_mesh.vao = hud_item_mesh.get_vao()

        # Render the cube
        hud_item_mesh.render()

        # Restore the chunk shader uniforms to their previous state
        shader["matrix_projection"].write(saved_projection)
        shader["matrix_view"].write(saved_view)
        shader["matrix_model"].write(saved_model)
        shader["shading_mode"].value = saved_shading_mode
        shader["textures_enabled"].value = saved_textures_enabled
        shader["skybox_color"].write(saved_skybox_color)
        shader["water_line"] = saved_water_line

    def set_uniforms_on_init(self) -> None:
        """
        Set initial values for shader uniforms that do not change frequently.
        """
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
