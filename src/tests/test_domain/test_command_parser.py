from domain.parser import SimpleCommandParser
from constants import Command

class TestSimpleCommandParser:
    def test_parse_single_forward_command(self):
        parser = SimpleCommandParser()
        result = parser.parse("F")
        assert result == [Command.F]
    
    def test_parse_single_left_command(self):
        parser = SimpleCommandParser()
        result = parser.parse("L")
        assert result == [Command.L]
    
    def test_parse_single_right_command(self):
        parser = SimpleCommandParser()
        result = parser.parse("R")
        assert result == [Command.R]
    
    def test_parse_multiple_commands(self):
        parser = SimpleCommandParser()
        result = parser.parse("FLR")
        assert result == [Command.F, Command.L, Command.R]
    
    def test_parse_complex_sequence(self):
        parser = SimpleCommandParser()
        result = parser.parse("FFRFFFRRL")
        expected = [Command.F, Command.F, Command.R, Command.F, Command.F, Command.F, Command.R, Command.R, Command.L]
        assert result == expected
    
    def test_parse_empty_string(self):
        parser = SimpleCommandParser()
        result = parser.parse("")
        assert result == []
    
    def test_parse_invalid_commands_ignored(self):
        parser = SimpleCommandParser()
        result = parser.parse("__21231dsadwaFXLYR")
        assert result == [Command.F, Command.L, Command.R]
