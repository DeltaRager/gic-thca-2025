from pydantic import BaseModel, field_validator
from .car import Car
from src.constants import Direction
from src.settings import settings

class Grid(BaseModel):
    size: int
    car_id: int = 0
    cars: dict = {}

    @field_validator('size')
    def check_size(cls, value):
        if value <= 0:
            raise ValueError('Size must be a positive integer')
        if value > settings.max_grid_size:
            raise ValueError(f'Size must not exceed MAX_GRID_SIZE={settings.max_grid_size}')
        return value
    
    def add_car(self, id: str, x: int, y: int, direction: Direction) -> None:
        if id in self.cars.keys():
            raise ValueError(f"Car with id '{id}' already exists")

        if not self.is_within_bounds(x, y):
            raise ValueError(f"Car position ({x}, {y}) is out of bounds on grid size {self.size}")

        car_obj = Car(x=x, y=y, direction=direction)
        self.cars[id] = car_obj

    def remove_car(self, id: str) -> None:
        if id not in self.cars:
            raise ValueError(f"Car with id '{id}' does not exist")
        del self.cars[id]

    def is_within_bounds(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size
