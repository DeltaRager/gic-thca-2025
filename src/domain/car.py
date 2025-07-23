from pydantic import BaseModel, ConfigDict, PrivateAttr, field_validator

from constants import Command, Direction

from .interfaces import CommandParser, MovementStrategy


class Car(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    x: int
    y: int
    direction: Direction = Direction.NORTH
    command_parser: CommandParser
    forward_strategy: MovementStrategy
    turn_strategy: MovementStrategy
    _commands: list[Command] = PrivateAttr(default_factory=list)

    @field_validator("x", "y")
    def must_be_non_negative(cls, value):
        if value < 0:
            raise ValueError("Coordinates must be non-negative")
        return value

    @field_validator("direction")
    def must_be_valid_direction(cls, value):
        if value not in Direction:
            raise ValueError("Invalid direction")
        return value

    @property
    def position(self) -> tuple[int, int]:
        return (self.x, self.y)

    @property
    def movement_vector(self) -> tuple[int, int]:
        return self.direction.value

    def add_commands(self, command_string: str) -> None:
        parsed_commands = self.command_parser.parse(command_string)
        self._commands.extend(parsed_commands)

    def get_next_command(self, current_step: int) -> Command:
        if current_step < len(self._commands):
            return self._commands[current_step]
        return None

    def calculate_command(self, command: Command) -> tuple[int, int, Direction]:
        if command == Command.F:
            return self.forward_strategy.execute(
                self.x, self.y, self.direction, command
            )
        elif command in (Command.L, Command.R):
            return self.turn_strategy.execute(self.x, self.y, self.direction, command)
        else:
            raise ValueError(f"Unknown command: {command}")

    def move(self, command: Command) -> None:
        x, y, direction = self.calculate_command(command)
        self.x = x
        self.y = y
        self.direction = direction
