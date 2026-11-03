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
python play.py --fast --no-verify # fastest possible, e.g. for a screen recording
```

`--fast` removes the mouse travel time and waits 1 ms between clicks, and
`--no-verify` skips the final re-read of the board. Both are faster but a
missed click is then neither prevented nor fixed.

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
- Symbols are detected by color, not by template matching, so the code does not
  depend on the size of the game on screen.

## Disclaimer

This is a recreational / educational project about computer vision and
constraint solving. Tango has daily rankings: do not use this script to post
scores or to compete against other players. Using automation on a website may
also go against its terms of service, so use it at your own risk and on
your own account only.
