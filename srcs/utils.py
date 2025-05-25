from pygame import SYSTEM_CURSOR_ARROW, cursors, mouse


def hide_cursor() -> None:
    """
    Hide the mouse cursor by setting a fully transparent cursor.
    """
    # Creates a fully transparent 8x8 cursor
    invisible_cursor = (
        (8, 8),  # size
        (0, 0),  # hotspot
        (0,) * 8,  # AND mask (no pixels visible)
        (0,) * 8,  # XOR mask (no pixels visible)
    )
    mouse.set_cursor(*invisible_cursor)


def show_cursor() -> None:
    """
    Show the mouse cursor by resetting it to the default arrow cursor.
    """
    mouse.set_cursor(SYSTEM_CURSOR_ARROW)
