"""Finds the Tango board on screen, solves it and clicks the solution.

    python play.py                    play on the live screen
    python play.py --dry-run          only analyse and save an annotated image
    python play.py --image shot.png   analyse a saved screenshot (no clicks)
"""
import argparse
import copy
import os
import sys
import time

import cv2

from automation import screen
from automation.overlay import annotate
from automation.planner import plan_clicks
from tango.solver import Solver
from vision.board_reader import BoardMisread, BoardNotFound, BoardReader


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--image", help="read this screenshot instead of the screen (implies --dry-run)")
    parser.add_argument("--dry-run", action="store_true", help="analyse and solve, but do not click")
    parser.add_argument("--wait", type=float, default=3.0,
                        help="seconds to switch to the game window before capturing (default: 3)")
    parser.add_argument("--monitor", type=int, help="monitor number to look at (default: all of them)")
    parser.add_argument("--click-interval", type=float, default=0.15,
                        help="seconds between two clicks (default: 0.15)")
    parser.add_argument("--retries", type=int, default=2,
                        help="extra passes if the board is not right after clicking (default: 2)")
    parser.add_argument("--debug-dir", default="debug",
                        help="where to save the capture and the annotated image (default: debug)")
    return parser.parse_args(argv)


def find_board(captures, reader):
    """First capture holding a readable board -> (capture, reading)."""
    misread = None

    for capture in captures:
        try:
            return capture, reader.read(capture.image)
        except BoardNotFound:
            continue
        except BoardMisread as error:
            misread = error

    if misread is not None:
        raise misread

    raise BoardNotFound("No Tango board found on screen")


def save_debug(args, capture, reading, solution, plan):
    os.makedirs(args.debug_dir, exist_ok=True)

    raw = os.path.join(args.debug_dir, "capture.png")
    annotated = os.path.join(args.debug_dir, "annotated.png")

    cv2.imwrite(raw, capture.image)
    cv2.imwrite(annotated, annotate(capture.image, reading.geometry, solution, plan))

    print(f"Saved {raw} and {annotated}")


def click_plan(capture, geometry, plan, interval):
    for row, col, clicks in plan:
        x, y = capture.to_screen(*geometry.cell_center(row, col))
        screen.click(x, y, clicks, interval)


def verify_and_fix(args, reader, solution):
    """Re-reads the screen and clicks again whatever is still wrong."""
    for attempt in range(args.retries + 1):
        time.sleep(0.6)

        try:
            capture, reading = find_board(screen.grab(args.monitor), reader)
        except (BoardNotFound, BoardMisread):
            print("Could not read the board back (a result screen may be covering it).")
            return

        plan = plan_clicks(reading.board, solution)

        if not plan:
            print("Board matches the solution.")
            return

        if attempt == args.retries:
            print(f"{len(plan)} cell(s) still differ after {args.retries + 1} passes: "
                  + ", ".join(f"({r},{c})" for r, c, _ in plan))
            return

        print(f"{len(plan)} cell(s) differ, clicking again...")
        click_plan(capture, reading.geometry, plan, args.click_interval)


def main(argv=None):
    args = parse_args(argv)
    dry_run = args.dry_run or args.image is not None
    reader = BoardReader()

    if args.image:
        image = cv2.imread(args.image)

        if image is None:
            sys.exit(f"Could not load image: {args.image}")

        captures = [screen.Capture(image)]
    else:
        screen.enable_dpi_awareness()

        if args.wait > 0:
            print(f"Switch to the game window, capturing in {args.wait:g}s...")
            time.sleep(args.wait)

        captures = screen.grab(args.monitor)

    try:
        capture, reading = find_board(captures, reader)
    except BoardNotFound:
        sys.exit("No Tango board found. Is the game visible, fully on screen, in light mode?")
    except BoardMisread as error:
        sys.exit(f"Found a board but could not read it properly.\n{error}")

    board = reading.board
    print("Puzzle read:\n" + str(board))
    print(f"{len(board.constraints)} constraint(s)")

    solver = Solver()
    solutions = solver.count_solutions(board)

    if solutions == 0:
        sys.exit("This puzzle has no solution. Some cells may already be filled in by hand: "
                 "press Clear in the game, or the board was misread (see the debug images).")

    if solutions > 1:
        print("Warning: several solutions fit what was read. A constraint was probably missed.")

    solution = copy.deepcopy(board)
    solver.solve(solution)

    print("Solution:\n" + str(solution))

    plan = plan_clicks(board, solution)

    if args.debug_dir:
        save_debug(args, capture, reading, solution, plan)

    if not plan:
        print("Nothing to click: the board already matches the solution.")
        return

    if dry_run:
        print(f"Dry run: {len(plan)} cell(s) would be clicked.")
        return

    print(f"Clicking {len(plan)} cell(s)...")
    click_plan(capture, reading.geometry, plan, args.click_interval)

    #--verify_and_fix(args, reader, solution)


if __name__ == "__main__":
    main()
