import cv2

from tango.enums import Symbol

LABELS = {Symbol.SUN: "S", Symbol.MOON: "M"}


def annotate(image, geometry, solution, plan):
    """Copy of the screenshot with the board outlined and each planned click.

    Every cell to click shows its target symbol and the number of clicks.
    """
    out = image.copy()

    x, y, size = geometry.x, geometry.y, geometry.size

    cv2.rectangle(out, (x, y), (x + size, y + size), (0, 160, 0), 3)

    scale = max(0.6, geometry.cell_size / 60)
    thickness = max(2, int(scale * 2))

    for row, col, clicks in plan:
        cx, cy = geometry.cell_center(row, col)
        text = f"{LABELS[solution.get_cell(row, col)]}x{clicks}"

        (w, h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, scale, thickness)
        origin = (int(cx - w / 2), int(cy + h / 2))

        cv2.putText(out, text, origin, cv2.FONT_HERSHEY_SIMPLEX, scale,
                    (255, 255, 255), thickness + 3)
        cv2.putText(out, text, origin, cv2.FONT_HERSHEY_SIMPLEX, scale,
                    (0, 0, 200), thickness)

    return out
