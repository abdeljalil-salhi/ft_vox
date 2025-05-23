from typing import TYPE_CHECKING
from moderngl import LINEAR, LINEAR_MIPMAP_LINEAR, Texture
from pygame import image, transform


if TYPE_CHECKING:
    from main import Engine


class Textures:
    def __init__(self, game: "Engine") -> None:
        self.game = game
        self.context = game.context

        self.notexture = self.load("frame.png")
        self.notexture.use(location=0)

    def load(self, file_name: str) -> Texture:
        texture = image.load(f"assets/{file_name}")
        texture = transform.flip(texture, flip_x=True, flip_y=False)

        texture = self.context.texture(
            size=texture.get_size(),
            components=4,
            data=image.tostring(texture, "RGBA", False),
        )
        texture.anisotropy = 32.0
        texture.build_mipmaps()
        texture.filter = (LINEAR_MIPMAP_LINEAR, LINEAR)
        return texture
