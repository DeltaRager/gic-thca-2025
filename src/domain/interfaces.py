from abc import ABC, abstractmethod
from typing import Protocol
from constants import Command, Direction

class Movable(Protocol):
    def move(self, command: Command) -> None: ...
    def calculate_command(self, command: Command) -> tuple[int, int, Direction]: ...

class CommandParser(ABC):
    @abstractmethod
    def parse(self, command_string: str) -> list[Command]: ...

class MovementStrategy(ABC):
    @abstractmethod
    def execute(self, x: int, y: int, direction: Direction, command: Command) -> tuple[int, int, Direction]: ...
