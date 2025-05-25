from typing import TYPE_CHECKING
from pygame import (
    K_LSHIFT,
    K_RSHIFT,
    MOUSEBUTTONDOWN,
    K_z,
    K_w,
    K_a,
    K_s,
    K_d,
    K_q,
    K_e,
    key,
    mouse,
)
from glm import vec3
from settings import (
    KEYBOARD_QWERTY,
    MOUSE_SENSITIVITY,
    PLAYER_POSITION,
    PLAYER_SPEED,
    WINDOW_RESOLUTION,
)

from srcs.camera import Camera

if TYPE_CHECKING:
    from srcs.engine import Engine


class Player(Camera):
    """
    A player controller class derived from the Camera class.

    Handles player-specific input (keyboard and mouse) to update camera position
    and orientation in a voxel-based world. Also interacts with the voxel world
    through mouse clicks (placing/removing blocks or switching modes).

    Attributes:
        game (Engine): Reference to the main game engine.
    """

    def __init__(
        self,
        game: "Engine",
        position: vec3 = PLAYER_POSITION,
        yaw: float = -90.0,
        pitch: float = 0.0,
    ) -> None:
        """
        Initialize the player with the game engine and camera parameters.

        Args:
            game (Engine): Game engine instance for accessing world and delta time.
            position (vec3): Starting position of the player.
            yaw (float): Initial yaw angle in degrees.
            pitch (float): Initial pitch angle in degrees.
        """
        self.game = game
        super().__init__(position, yaw, pitch)

    def on_init(self) -> None:
        """
        Should be called once at the start of the game.
        Used to check for collision in Camera level.
        """
        self.world = self.game.scene.world

    def update(self) -> None:
        """
        Update the player's state based on input events and call camera update logic.
        Should be called every frame.
        """
        self.keyboard_events()
        self.mouse_events()
        super().update()

    def handle_mouse_events(self, event) -> None:
        """
        Handle mouse button press events for interacting with the voxel world.

        Args:
            event: Pygame mouse event.
        """
        if event.type == MOUSEBUTTONDOWN:
            voxel_handler = self.game.scene.world.voxel_handler
            if event.button == 1:  # Left-click: place or remove voxel
                voxel_handler.set_voxel()
            elif event.button == 3:  # Right-click: switch interaction mode
                voxel_handler.switch_interaction_mode()

    def mouse_events(self) -> None:
        """
        Handle mouse movement for adjusting the player's camera rotation.
        Re-centers the mouse to the screen after reading input.
        """
        mouse_dx, mouse_dy = mouse.get_rel()

        if mouse_dx:
            self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)

        # Reset mouse position to center of screen for continuous input
        mouse.set_pos(WINDOW_RESOLUTION.x * 0.5, WINDOW_RESOLUTION.y * 0.5)

    def keyboard_events(self) -> None:
        """
        Handle keyboard input to move the player based on current key states.
        Supports sprinting and different layouts (QWERTY/AZERTY).
        """
        key_state = key.get_pressed()

        # Sprinting when holding either shift key
        speed_multiplier = 2.0 if key_state[K_LSHIFT] or key_state[K_RSHIFT] else 1.0
        velocity = self.game.delta_time * PLAYER_SPEED * speed_multiplier

        # Forward movement (W or Z depending on layout)
        if key_state[K_w if KEYBOARD_QWERTY else K_z]:
            self.move_forward(velocity)

        # Backward movement (S)
        if key_state[K_s]:
            self.move_backward(velocity)

        # Right strafe (D)
        if key_state[K_d]:
            self.move_right(velocity)

        # Left strafe (A or Q depending on layout)
        if key_state[K_a if KEYBOARD_QWERTY else K_q]:
            self.move_left(velocity)

        # Upward movement (E)
        if key_state[K_e]:
            self.move_up(velocity)

        # Downward movement (Q or A depending on layout)
        if key_state[K_q if KEYBOARD_QWERTY else K_a]:
            self.move_down(velocity)
