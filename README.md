# tango_solver

**Small recreational project :**

- _Will try to implement a solver for the LinkedIn game Tango_

- _This repo will also be a toy to try GitLab -> GitHub mirroring_

## What it does

`play.py` looks for the Tango board anywhere on your screen (any window, any
size), reads the givens and the `=` / `x` signs, solves the puzzle and clicks
the solution. It then reads the board again and fixes any cell that did not
register.

Light mode only for now.

## Usage

```
pip install -r requirements.txt

python play.py                    # find the board, solve, click
python play.py --dry-run          # same, without clicking (see debug/annotated.png)
python play.py --image shot.png   # work on a saved screenshot, no clicks
```

Start from a fresh puzzle (press Clear if you already filled cells by hand),
keep the game fully visible, and run the script: it waits 3 seconds
(`--wait`) so you can leave the terminal and show the game window. Throw the
mouse into a screen corner to abort.

Run the tests with `python -m pytest` (or `python -m unittest`).

## How it works

- `vision/grid_detector.py`: finds the 6x6 grid by fitting its 5 + 5 interior
  lines, so it does not depend on colors or on a fixed size.
- `vision/symbol_detector.py`: sun = orange pixels, moon = blue pixels.
- `vision/constraint_detector.py`: looks at the line between two cells for a
  `=` or `x` sign.
- `tango/`: board, rules and backtracking solver.
- `automation/`: screen capture, click planning (a click cycles empty, sun,
  moon, empty) and the mouse.

## Notes

- Windows, macOS (Retina included) and Linux/X11 are handled. Wayland is not.
  macOS asks for Screen Recording and Accessibility permissions.
- `assets/templates/` and `vision/extract_templates.py` are no longer used:
  symbols are detected by color instead of template matching.
