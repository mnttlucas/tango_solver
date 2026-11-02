def clicks_needed(current, target):
    """Clicks to turn a cell from `current` into `target`.

    In Tango a click cycles a cell EMPTY -> SUN -> MOON -> EMPTY, which is
    exactly the order of the Symbol values (0, 1, 2).
    """
    return (target.value - current.value) % 3


def plan_clicks(current, solution):
    """List of (row, col, clicks) to go from the displayed board to `solution`.

    Cells already right need no click, so planning again after a partial or
    failed attempt only clicks what is still wrong.
    """
    plan = []

    for row in range(solution.size):
        for col in range(solution.size):
            clicks = clicks_needed(
                current.get_cell(row, col), solution.get_cell(row, col)
            )

            if clicks:
                plan.append((row, col, clicks))

    return plan
