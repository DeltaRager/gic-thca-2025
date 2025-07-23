from pydantic import BaseModel, field_validator, PrivateAttr
from src.constants import Direction, DirectionMap, Command
from .grid import Grid

class Car(BaseModel):
    x: int
    y: int
    direction: Direction = Direction.NORTH  
    _commands: list[str] = PrivateAttr([])

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
    
    @property
    def movement_vector(self) -> tuple[int, int]:
        return self.direction.value
    
    def add_command(self, command: str) -> None:
        commands = command.split('')
        for cmd in commands:
            if cmd == 'F':
                self._commands.append(Command.F)
            elif cmd in (Command.L, Command.R):
                self._commands.append(Command(cmd))

        self._commands.append(command)

    def calculate_command(self, command: Command) -> None:
        new_x, new_y = self.x, self.y
        new_direction = self.direction
        if command == Command.F:
            dx, dy = self.movement_vector
            new_x += dx
            new_y += dy
        elif command in (Command.L, Command.R):
            try:
                new_direction = DirectionMap.turn_map[self.direction][command]
            except KeyError:
                raise ValueError(
                    f"Invalid turn '{command}' for direction '{self.direction}'"
                )
        else:
            raise ValueError(f"Unknown command: {command}")
        
        return new_x, new_y, new_direction
    
    def move(self, command: Command, grid: Grid) -> None:
        x, y, direction = self.calculate_command(command)

        if not grid.is_within_bounds(x, y):
            raise ValueError(f"Move out of bounds: ({x}, {y}) on grid size {grid.size}")

        self.x = x
        self.y = y
        self.direction = direction
