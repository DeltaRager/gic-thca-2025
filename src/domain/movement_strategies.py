from .interfaces import MovementStrategy
from constants import Command, Direction, DirectionMap

class ForwardMovementStrategy(MovementStrategy):
    def execute(self, x: int, y: int, direction: Direction, command: Command) -> tuple[int, int, Direction]:
        if command != Command.F:
            raise ValueError(f"ForwardMovementStrategy cannot handle {command}")
        dx, dy = direction.value
        return x + dx, y + dy, direction

class TurnMovementStrategy(MovementStrategy):
    def execute(self, x: int, y: int, direction: Direction, command: Command) -> tuple[int, int, Direction]:
        if command not in (Command.L, Command.R):
            raise ValueError(f"TurnMovementStrategy cannot handle {command}")
        new_direction = DirectionMap.turn_map[direction][command]
        return x, y, new_direction