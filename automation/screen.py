import sys
import time

import numpy as np


class Capture:
    """A screenshot of one monitor, and how to get back to screen coordinates.

    `scale` is image pixels per screen unit: 1 on most setups, 2 on a Retina
    Mac (screenshots are in pixels, mouse coordinates are in points).
    """

    def __init__(self, image, left=0, top=0, scale=1.0):
        self.image = image
        self.left = left
        self.top = top
        self.scale = scale

    def to_screen(self, x, y):
        """Image pixel -> position to give to the mouse."""
        return (self.left + x / self.scale, self.top + y / self.scale)


def enable_dpi_awareness():
    """Windows: make screenshots and the mouse use the same physical pixels."""
    if sys.platform != "win32":
        return

    try:
        import ctypes

        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        pass


def grab(monitor=None):
    """Yields a Capture for the given monitor number, or for each monitor.

    Monitor numbers are mss's: 1 is the primary one, 2 the next, and so on.
    """
    import mss

    with mss.mss() as sct:
        numbers = [monitor] if monitor else range(1, len(sct.monitors))

        for number in numbers:
            info = sct.monitors[number]
            shot = sct.grab(info)

            image = np.ascontiguousarray(np.array(shot)[:, :, :3])  # BGRA -> BGR
            scale = shot.width / info["width"]

            yield Capture(image, info["left"], info["top"], scale)


def click(x, y, times=1, interval=0.15, move_duration=0.05):
    """Moves the mouse there and clicks `times` times, `interval` seconds apart.

    Spacing the clicks out keeps the page from seeing a double-click; a very
    small interval is faster but riskier. Moving the mouse into a screen
    corner aborts the script (pyautogui's fail-safe).
    """
    import pyautogui

    pyautogui.moveTo(x, y, duration=move_duration)

    for _ in range(times):
        pyautogui.click()
        time.sleep(interval)
