from glm import radians, vec2, vec3
from math import atan, tan, sqrt


# GAME SETTINGS
WINDOW_TITLE = "ft_vox"
WINDOW_RESOLUTION = vec2(1920, 1080)
KEYBOARD_QWERTY = False  # Set to False for AZERTY keyboard layout
SHOW_CHUNKS = False
GO_THROUGH = False


# CAMERA SETTINGS
ASPECT_RATIO = WINDOW_RESOLUTION.x / WINDOW_RESOLUTION.y
FOV_DEGREES = 50.0
VERTICAL_FOV = radians(FOV_DEGREES)
HORIZONTAL_FOV = 2.0 * atan(tan(VERTICAL_FOV * 0.5) * ASPECT_RATIO)
NEAR = 0.1
FAR = 2000.0
PITCH_LIMIT = radians(89.0)
MAX_RAY_DISTANCE = 6.0


# WORLD SETTINGS
SEED = 16

CHUNK_SIZE = 48
H_CHUNK_SIZE = CHUNK_SIZE // 2
CHUNK_AREA = CHUNK_SIZE * CHUNK_SIZE
CHUNK_VOLUME = CHUNK_SIZE * CHUNK_AREA
CHUNK_SPHERE_RADIUS = H_CHUNK_SIZE * sqrt(3.0)

WORLD_WIDTH, WORLD_HEIGHT = 100, 2
WORLD_DEPTH = WORLD_WIDTH
WORLD_AREA = WORLD_WIDTH * WORLD_DEPTH
WORLD_VOLUME = WORLD_HEIGHT * WORLD_AREA

CENTER_XZ = WORLD_WIDTH * H_CHUNK_SIZE
CENTER_Y = WORLD_HEIGHT * H_CHUNK_SIZE


# PLAYER SETTINGS
PLAYER_WIDTH = 0.6
PLAYER_HEIGHT = 1.8
PLAYER_DEPTH = 0.6
PLAYER_SPEED = 0.02
PLAYER_ROTATION_SPEED = 0.003
PLAYER_POSITION = vec3(CENTER_XZ, WORLD_HEIGHT * CHUNK_SIZE, CENTER_XZ)

MOUSE_SENSITIVITY = 0.002
EYE_HEIGHT = 1.6
COLLISION_OFFSET = 0.1
