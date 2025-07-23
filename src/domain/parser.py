from constants import Command

from .interfaces import CommandParser


class SimpleCommandParser(CommandParser):
    def parse(self, command_string: str) -> list[Command]:
        commands = []
        for cmd in command_string:
            if cmd == "F":
                commands.append(Command.F)
            elif cmd == "L":
                commands.append(Command.L)
            elif cmd == "R":
                commands.append(Command.R)

        return commands
