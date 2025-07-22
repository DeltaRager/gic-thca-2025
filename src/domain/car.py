from pydantic import BaseModel, field_validator
from src.constants import Direction

class Car(BaseModel):
    x: int
    y: int
    direction: Direction = Direction.NORTH

    @field_validator('x', 'y')
    def must_be_non_negative(cls, value):
        if value < 0:
            raise ValueError('Coordinates must be non-negative')
        return value
    
    @field_validator('direction')
    def must_be_valid_direction(cls, value):
        if value not in Direction:
            raise ValueError('Invalid direction')
        return value

    @property
    def position(self) -> tuple[int, int]:
        return (self.x, self.y)
