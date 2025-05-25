from functools import cache
from pygame import (
    ACTIVEEVENT,
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
    K_h,
    K_t,
    K_1,
    K_2,
    K_3,
    K_4,
    K_5,
    K_6,
    K_7,
    K_8,
    K_9,
    K_0,
    init,
    quit,
    display,
    event,
    mouse,
    time,
)
from moderngl import BLEND, CULL_FACE, DEPTH_TEST, create_context
from sys import exit

from objects.inventory import Inventory
from objects.texturing import SKYBOX_COLOR
from settings import WINDOW_RESOLUTION, WINDOW_TITLE
from srcs.mixer import Mixer
from srcs.player import Player
from srcs.scene import Scene
from srcs.shader import Shader
from srcs.textures import Textures
from srcs.utils import hide_cursor, show_cursor


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
        hide_cursor()

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

        self.shading_mode = 2
        self.textures_enabled = True

        self.on_init()

    def get_textures_enabled(self) -> bool:
        return self.textures_enabled

    @cache
    def get_window_resolution(self) -> tuple[int, int]:
        w, h = display.get_surface().get_size()
        return w, h

    def show_loading_screen(self) -> None:
        self.context.clear(color=SKYBOX_COLOR)
        display.flip()

    def on_init(self) -> None:
        self.show_loading_screen()

        self.textures = Textures(self)
        self.player = Player(self)
        self.inventory = Inventory(self)
        self.shader = Shader(self)
        self.scene = Scene(self)
        self.mixer = Mixer()

        self.player.on_init()

        self.shader.chunk["shading_mode"].value = self.shading_mode
        self.shader.chunk["textures_enabled"].value = self.textures_enabled

    def update(self) -> None:
        self.player.update()
        self.shader.update()
        self.scene.update()

        self.delta_time = self.clock.tick()
        self.time = time.get_ticks() * 0.001
        display.set_caption(f"{WINDOW_TITLE} - {self.clock.get_fps():.0f}fps")

    def render(self) -> None:
        self.context.clear(color=SKYBOX_COLOR)
        self.scene.render()
        display.flip()

    def handle_events(self) -> None:
        for e in event.get():
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                self.is_running = False
            if e.type == ACTIVEEVENT:
                if e.gain:
                    mouse.set_visible(False)
                    hide_cursor()
                else:
                    mouse.set_visible(True)
                    show_cursor()
            if e.type == KEYDOWN:
                if e.key == K_h:
                    self.shading_mode = (self.shading_mode - 1) % 3
                    self.shader.chunk["shading_mode"].value = self.shading_mode
                elif e.key == K_t:
                    self.textures_enabled = not self.textures_enabled
                    self.shader.chunk["textures_enabled"].value = self.textures_enabled
                if e.key == K_1:
                    self.inventory.select_slot(0)
                elif e.key == K_2:
                    self.inventory.select_slot(1)
                elif e.key == K_3:
                    self.inventory.select_slot(2)
                elif e.key == K_4:
                    self.inventory.select_slot(3)
                elif e.key == K_5:
                    self.inventory.select_slot(4)
                elif e.key == K_6:
                    self.inventory.select_slot(5)
                elif e.key == K_7:
                    self.inventory.select_slot(6)
                elif e.key == K_8:
                    self.inventory.select_slot(7)
                elif e.key == K_9:
                    self.inventory.select_slot(8)
                elif e.key == K_0:
                    self.inventory.select_slot(9)
            self.player.handle_mouse_events(e)

    def run(self) -> None:
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
            self.mixer.play_soundtrack()
        show_cursor()
        quit()
        exit()
