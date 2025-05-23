from typing import TYPE_CHECKING
from pygame import K_z, K_w, K_a, K_s, K_d, K_q, K_e, key, mouse
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
    from main import Engine


class Player(Camera):
    def __init__(
        self,
        game: "Engine",
        position: vec3 = PLAYER_POSITION,
        yaw: float = -90.0,
        pitch: float = 0.0,
    ) -> None:
        self.game = game
        super().__init__(position, yaw, pitch)

    def update(self) -> None:
        self.keyboard_events()
        self.mouse_events()
        super().update()

    def mouse_events(self) -> None:
        mouse_dx, mouse_dy = mouse.get_rel()
        if mouse_dx:
            self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)
        mouse.set_pos(WINDOW_RESOLUTION.x * 0.5, WINDOW_RESOLUTION.y * 0.5)

    def keyboard_events(self) -> None:
        key_state = key.get_pressed()
        velocity = self.game.delta_time * PLAYER_SPEED
        if key_state[K_w if KEYBOARD_QWERTY else K_z]:
            self.move_forward(velocity)
        if key_state[K_s]:
            self.move_backward(velocity)
        if key_state[K_d]:
            self.move_right(velocity)
        if key_state[K_a if KEYBOARD_QWERTY else K_q]:
            self.move_left(velocity)
        if key_state[K_e]:
            self.move_up(velocity)
        if key_state[K_q if KEYBOARD_QWERTY else K_a]:
            self.move_down(velocity)
