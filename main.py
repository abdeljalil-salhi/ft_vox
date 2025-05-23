from pygame import (
    DOUBLEBUF,
    FULLSCREEN,
    GL_CONTEXT_MAJOR_VERSION,
    GL_CONTEXT_MINOR_VERSION,
    GL_CONTEXT_PROFILE_CORE,
    GL_CONTEXT_PROFILE_MASK,
    GL_DEPTH_SIZE,
    K_ESCAPE,
    KEYDOWN,
    OPENGL,
    QUIT,
    init,
    quit,
    display,
    event,
    mouse,
    time,
)
from moderngl import BLEND, CULL_FACE, DEPTH_TEST, create_context
from sys import exit

from settings import SKYBOX_COLOR, WINDOW_RESOLUTION
from srcs.scene import Scene
from srcs.shader import Shader


class Engine:
    def __init__(self) -> None:
        init()

        # Use OpenGL 3.3 Core Profile (removes deprecated functionality from earlier versions)
        display.gl_set_attribute(GL_CONTEXT_MAJOR_VERSION, 3)
        display.gl_set_attribute(GL_CONTEXT_MINOR_VERSION, 3)
        display.gl_set_attribute(GL_CONTEXT_PROFILE_MASK, GL_CONTEXT_PROFILE_CORE)

        # Set the depth buffer size to 24 bits
        # This is important for 3D rendering to avoid z-fighting
        display.gl_set_attribute(GL_DEPTH_SIZE, 24)

        display.set_mode(
            WINDOW_RESOLUTION, flags=FULLSCREEN | OPENGL | DOUBLEBUF
        )  # double buffering for smoother rendering

        event.set_grab(True)  # locks the mouse to the window
        mouse.set_visible(False)
        mouse.set_pos(WINDOW_RESOLUTION.x // 2, WINDOW_RESOLUTION.y // 2)

        self.context = create_context()
        # DEPTH_TEST:
        #     Ensures that fragments (pixels) that are closer to the camera are drawn in front of those that are farther away.
        # CULL_FACE:
        #     Discards faces of triangles that are not visible to the camera, improving performance.
        # BLEND:
        #     Allows for transparency effects by blending the color of a fragment with the color of the pixel already in the framebuffer.
        self.context.enable(
            flags=DEPTH_TEST | CULL_FACE | BLEND
        )  # correctly (depth), efficiently (culling), beautifully (blending)
        self.context.gc_mode = (
            "auto"  # automatic garbage collection to prevent memory leaks
        )

        self.clock = time.Clock()
        self.delta_time = 0.0
        self.time = 0.0
        self.is_running = True

        self.on_init()

    def show_loading_screen(self) -> None:
        self.context.clear(color=SKYBOX_COLOR)
        display.flip()

    def on_init(self) -> None:
        self.show_loading_screen()

        # TODO: Initialize game objects and resources here
        # For example, load shaders, textures, etc.
        self.shader = Shader(self)
        self.scene = Scene(self)

    def update(self) -> None:
        self.shader.update()
        self.scene.update()

        self.delta_time = self.clock.tick()
        self.time = time.get_ticks() * 0.001
        display.set_caption(f"ft_vox - {self.clock.get_fps():.0f}fps")

    def render(self) -> None:
        self.context.clear(color=SKYBOX_COLOR)
        self.scene.render()
        display.flip()

    def handle_events(self) -> None:
        for e in event.get():
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                self.is_running = False
            # TODO: Handle other events here
            # For example, mouse movement, keyboard input, etc.

    def run(self) -> None:
        print("Engine is running")
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
        quit()
        exit()


if __name__ == "__main__":
    engine = Engine()
    engine.run()
