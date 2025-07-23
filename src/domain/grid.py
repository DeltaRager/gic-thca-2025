import logging

from pydantic import BaseModel, field_validator

from constants import Direction
from settings import settings

from .car import Car
from .movement_strategies import ForwardMovementStrategy, TurnMovementStrategy
from .parser import SimpleCommandParser


class Grid(BaseModel):
    size_x: int = settings.max_grid_size_x
    size_y: int = settings.max_grid_size_y
    cars: dict = {}
    current_step: int = 0

    @property
    def logger(self):
        return logging.getLogger(__name__)

    @field_validator("size_x")
    def check_size_x(cls, value):
        if value <= 0:
            raise ValueError("Grid size_x must be a positive integer")
        if value > settings.max_grid_size_x:
            raise ValueError(f"Grid size_x cannot exceed {settings.max_grid_size_x}")
        return value

    @field_validator("size_y")
    def check_size_y(cls, value):
        if value <= 0:
            raise ValueError("Grid size_y must be a positive integer")
        if value > settings.max_grid_size_y:
            raise ValueError(f"Grid size_y cannot exceed {settings.max_grid_size_y}")
        return value

    def is_within_bounds(self, x, y):
        return 0 <= x < self.size_x and 0 <= y < self.size_y

    def add_car(
        self, id: str, x: int, y: int, direction: Direction, commands: str
    ) -> None:
        if len(self.cars.keys()) >= self.size_x * self.size_y:
            raise ValueError("Cannot add more cars than the grid can hold")

        for car_id, car in self.cars.items():
            if car.position == (x, y):
                raise ValueError(
                    f"Position ({x}, {y}) is already occupied by car {car_id}"
                )

        if id in self.cars.keys():
            raise ValueError(f"Car with id '{id}' already exists")

        if not self.is_within_bounds(x, y):
            raise ValueError(
                f"Car position ({x}, {y}) is out of bounds on grid size {self.size_x}x{self.size_y}"
            )

        command_parser = SimpleCommandParser()
        forward_strategy = ForwardMovementStrategy()
        turn_strategy = TurnMovementStrategy()

        car_obj = Car(
            x=x,
            y=y,
            direction=direction,
            command_parser=command_parser,
            forward_strategy=forward_strategy,
            turn_strategy=turn_strategy,
        )
        car_obj.add_commands(commands)
        self.cars[id] = car_obj

    def remove_car(self, id: str) -> None:
        if id not in self.cars:
            raise ValueError(f"Car with id '{id}' does not exist")
        del self.cars[id]

    def check_collisions(self):
        positions = {}
        for car_id, car in self.cars.items():
            pos = car.position
            if pos in positions:
                positions[pos].append(car_id)
            else:
                positions[pos] = [car_id]

        for pos, car_ids in positions.items():
            if len(car_ids) > 1:
                self.logger.debug(
                    f"Collision detected at position {pos} between cars: {', '.join(car_ids)}"
                )
                for car_id in car_ids:
                    print(car_id, end=" ")
                print()
                print(f"{pos[0]} {pos[1]}")
                print(self.current_step)
                return {"collision": True, "cars": car_ids, "position": pos}

        self.logger.debug("No collisions detected")

        return {"collision": False}

    def next_step(self) -> None:
        for car_id, car in self.cars.items():
            command = car.get_next_command(self.current_step)
            if command is None:
                logging.getLogger(__name__).debug(
                    f"Car {car_id} has no more commands to execute"
                )
                continue
            new_x, new_y, new_direction = car.calculate_command(command)
            if self.is_within_bounds(new_x, new_y):
                car.move(command)
                logging.getLogger(__name__).debug(
                    f"Executing command {command} for car {car_id} at step {self.current_step}"
                )
                logging.getLogger(__name__).debug(
                    f"Car {car_id} moved to ({new_x}, {new_y}) facing {new_direction}"
                )
            else:
                logging.getLogger(__name__).warning(
                    f"Car {car_id} cannot move to ({new_x}, {new_y}) - out of bounds"
                )

        self.current_step += 1

        return self.check_collisions()
