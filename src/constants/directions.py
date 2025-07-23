from enum import Enum
from .commands import Command

class Direction(Enum):
    NORTH = (0, 1)
    SOUTH = (0, -1)
    EAST = (1, 0)
    WEST = (-1, 0)

class DirectionMap:
    turn_map = {
        Direction.NORTH: {Command.L: Direction.WEST, Command.R: Direction.EAST},
        Direction.EAST: {Command.L: Direction.NORTH, Command.R: Direction.SOUTH},
        Direction.SOUTH: {Command.L: Direction.EAST, Command.R: Direction.WEST},
        Direction.WEST: {Command.L: Direction.SOUTH, Command.R: Direction.NORTH},
    }
    

