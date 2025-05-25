from typing import TYPE_CHECKING
from moderngl import NEAREST, Texture
from pygame import SRCALPHA, image, transform, font, Surface

if TYPE_CHECKING:
    from srcs.engine import Engine


class Textures:
    def __init__(self, game: "Engine") -> None:
        self.game = game
        self.context = game.context

        # Load static textures
        self.no_texture = self.load("frame")
        self.texture_array = self.load("textures", is_texture_array=True)
        self.water_texture = self.load("water")

        # Initialize font and dynamic text texture
        self.font = font.Font(None, 24)  # Default font, size 24 for pixelated look
        # If you have Minecraft.ttf, uncomment the following line:
        # self.font = font.Font("assets/Minecraft.ttf", 24)
        self.text_texture = None  # Will be updated dynamically
        self.text_surface = None  # Keep surface for updates

        # Assign texture units for static textures
        self.no_texture.use(location=0)
        self.texture_array.use(location=1)
        self.water_texture.use(location=2)

    def load(self, file_name: str, is_texture_array: bool = False) -> Texture:
        texture = image.load(f"assets/{file_name}.png")
        texture = transform.flip(texture, flip_x=True, flip_y=False)

        if is_texture_array:
            # 3 layers for each texture
            num_layers = 3 * texture.get_height() // texture.get_width()
            texture = self.game.context.texture_array(
                size=(
                    texture.get_width(),
                    texture.get_height() // num_layers,
                    num_layers,
                ),
                components=4,
                data=image.tostring(texture, "RGBA", False),
            )
        else:
            texture = self.context.texture(
                size=texture.get_size(),
                components=4,
                data=image.tostring(texture, "RGBA", False),
            )

        texture.anisotropy = 32.0
        texture.build_mipmaps()
        texture.filter = (NEAREST, NEAREST)

        return texture

    def update_text(self, text: str) -> None:
        """Update the text texture with the given string, handling newlines."""
        # Split the text into lines based on newline characters
        lines = text.split("\n")
        if not lines:
            lines = [""]  # Ensure at least one line to avoid empty surface

        # Render each line to a separate surface
        line_surfaces = []
        max_width = 0
        for line in lines:
            if line:
                surface = self.font.render(
                    line, True, (255, 255, 255), (0, 0, 0, 0)
                )  # White text, transparent background
            else:
                # Handle empty lines by creating a transparent surface with the height of a space
                surface = Surface((1, self.font.get_linesize()), flags=SRCALPHA)
                surface.fill((0, 0, 0, 0))
            line_surfaces.append(surface)
            max_width = max(max_width, surface.get_width())

        # Calculate total height based on the number of lines and line spacing
        line_height = self.font.get_linesize()
        total_height = line_height * len(lines)

        # Create a single surface to hold all lines
        self.text_surface = Surface((max_width, total_height), flags=SRCALPHA)
        self.text_surface.fill((0, 0, 0, 0))

        # Blit each line onto the combined surface
        for i, surface in enumerate(line_surfaces):
            self.text_surface.blit(surface, (0, i * line_height))

        # Flip the surface vertically to match OpenGL's texture coordinate system
        self.text_surface = transform.flip(self.text_surface, False, True)

        if self.text_texture:
            self.text_texture.release()  # Release old texture to avoid memory leak
        self.text_texture = self.context.texture(
            size=self.text_surface.get_size(),
            components=4,
            data=image.tostring(self.text_surface, "RGBA", False),
        )
        self.text_texture.filter = (NEAREST, NEAREST)
        self.text_texture.use(location=3)
