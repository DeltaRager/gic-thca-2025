import logging
import sys

from application import Simulation
from settings import settings


def show_format_help():
    print("ERROR: Invalid input format!")
    print("\nCorrect format:")
    print("Line 1: grid_size_x grid_size_y")
    print("Then for each car:")
    print("  - Car ID (single character or string)")
    print("  - Starting position: x y direction")
    print("  - Commands (optional, can be empty line)")
    print("  - Empty line between cars (optional)")
    print("\nExample:")
    print("10 10")
    print("")
    print("A")
    print("1 2 N")
    print("FFRFFFFFRL")
    print("")
    print("B")
    print("7 8 W")
    print("FFLFFFFFFF")
    print("")
    print("C")
    print("5 4 S")
    print("")
    print("\nDirections: N (North), S (South), E (East), W (West)")
    print("Commands: F (Forward), L (Left turn), R (Right turn)")


def main():
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )
    logger = logging.getLogger(__name__)

    if len(sys.argv) != 2:
        print("ERROR: Missing input file!")
        print("Usage: python main.py <input_file>")
        sys.exit(1)

    try:
        with open(sys.argv[1], "r") as file:
            lines = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"ERROR: File '{sys.argv[1]}' not found!")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Could not read file '{sys.argv[1]}': {e}")
        sys.exit(1)

    # Remove leading/trailing empty lines
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()

    if not lines:
        print("ERROR: Empty input file!")
        show_format_help()
        sys.exit(1)

    # Parse grid size
    try:
        grid_parts = lines[0].split()
        if len(grid_parts) != 2:
            raise ValueError("Grid size must have exactly 2 numbers")
        grid_size_x, grid_size_y = map(int, grid_parts)
        if grid_size_x <= 0 or grid_size_y <= 0:
            raise ValueError("Grid dimensions must be positive")
    except (ValueError, IndexError) as e:
        print(f"ERROR: Invalid grid size format: '{lines[0]}'")
        print(f"Expected: two positive integers (e.g., '10 10')")
        show_format_help()
        sys.exit(1)

    # Parse cars
    cars = []
    i = 1
    car_number = 1

    while i < len(lines):
        # Skip empty lines between cars
        while i < len(lines) and not lines[i]:
            i += 1

        if i >= len(lines):
            break

        # Car ID
        car_id = lines[i]
        if not car_id:
            print(f"ERROR: Car {car_number} has empty ID at line {i+1}")
            show_format_help()
            sys.exit(1)
        i += 1

        # Position and direction
        if i >= len(lines):
            print(
                f"ERROR: Car {car_number} ('{car_id}') missing position and direction"
            )
            show_format_help()
            sys.exit(1)

        try:
            pos_parts = lines[i].split()
            if len(pos_parts) != 3:
                raise ValueError("Position must have exactly 3 parts: x y direction")
            x, y, direction = int(pos_parts[0]), int(pos_parts[1]), pos_parts[2].upper()
            if x < 0 or y < 0:
                raise ValueError("Coordinates must be non-negative")
            if direction not in ["N", "S", "E", "W"]:
                raise ValueError("Direction must be N, S, E, or W")
        except (ValueError, IndexError) as e:
            print(
                f"ERROR: Car {car_number} ('{car_id}') has invalid position/direction: '{lines[i]}'"
            )
            print(f"Expected format: 'x y direction' (e.g., '1 2 N')")
            show_format_help()
            sys.exit(1)

        position_direction = lines[i]
        i += 1

        # Commands (could be empty)
        commands = ""
        if i < len(lines) and lines[i]:
            # Check if this line looks like a car ID (next line would be position)
            is_next_car = (
                i + 1 < len(lines) and lines[i + 1] and len(lines[i + 1].split()) == 3
            )

            if not is_next_car:
                commands = lines[i]
                # Validate commands contain only F, L, R
                for cmd in commands:
                    if cmd not in "FLR":
                        print(
                            f"ERROR: Car {car_number} ('{car_id}') has invalid command '{cmd}' in '{commands}'"
                        )
                        print(
                            "Commands must contain only F (Forward), L (Left), R (Right)"
                        )
                        show_format_help()
                        sys.exit(1)
                i += 1

        cars.append([car_id, position_direction, commands])
        car_number += 1

    if not cars:
        print("ERROR: No cars found in input file!")
        show_format_help()
        sys.exit(1)

    logger.info(f"Grid size: {grid_size_x}x{grid_size_y}")
    for car in cars:
        logger.info(f"Car data: {car}")

    try:
        simulation = Simulation(
            grid_size_x=grid_size_x, grid_size_y=grid_size_y, cars=cars
        )

        simulation.run()
    except Exception as e:
        print(f"ERROR: Simulation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
