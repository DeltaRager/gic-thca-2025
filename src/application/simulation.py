import logging

from constants import Direction
from domain import Grid


def parse_direction(direction_str):
    direction_map = {
        "N": Direction.NORTH,
        "S": Direction.SOUTH,
        "E": Direction.EAST,
        "W": Direction.WEST,
    }
    return direction_map[direction_str.upper()]


class Simulation:
    def __init__(self, grid_size_x: int, grid_size_y: int, cars: list):
        self.logger = logging.getLogger(__name__)
        self.grid = Grid(size_x=grid_size_x, size_y=grid_size_y)

        self.max_step = 0

        for car in cars:
            car_id, init_state, commands = car
            init_state = init_state.split()

            self.max_step = max(self.max_step, len(commands))

            self.grid.add_car(
                id=car_id,
                x=int(init_state[0]),
                y=int(init_state[1]),
                direction=parse_direction(init_state[2]),
                commands=commands,
            )

    def run(self):
        collision_detected = False
        self.logger.info("Starting simulation...")

        for step in range(self.max_step):
            self.logger.debug(f"Step {step + 1}:")
            collision_result = self.grid.next_step()
            collision_detected = collision_result["collision"]
            self.logger.debug("-" * 20)
            if collision_detected:
                break

        if not collision_detected:
            print("no collision")

        self.logger.info("Simulation complete.")
