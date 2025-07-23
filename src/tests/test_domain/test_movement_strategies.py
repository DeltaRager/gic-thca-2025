from constants import Command, Direction
from domain.movement_strategies import ForwardMovementStrategy, TurnMovementStrategy


class TestForwardMovementStrategy:
    def test_execute_forward_north(self):
        strategy = ForwardMovementStrategy()
        x, y, direction = strategy.execute(0, 0, Direction.NORTH, Command.F)
        assert x == 0
        assert y == 1
        assert direction == Direction.NORTH

    def test_execute_forward_east(self):
        strategy = ForwardMovementStrategy()
        x, y, direction = strategy.execute(1, 1, Direction.EAST, Command.F)
        assert x == 2
        assert y == 1
        assert direction == Direction.EAST

    def test_execute_forward_south(self):
        strategy = ForwardMovementStrategy()
        x, y, direction = strategy.execute(2, 2, Direction.SOUTH, Command.F)
        assert x == 2
        assert y == 1
        assert direction == Direction.SOUTH

    def test_execute_forward_west(self):
        strategy = ForwardMovementStrategy()
        x, y, direction = strategy.execute(1, 1, Direction.WEST, Command.F)
        assert x == 0
        assert y == 1
        assert direction == Direction.WEST

    def test_execute_invalid_command_raises_error(self):
        strategy = ForwardMovementStrategy()
        try:
            strategy.execute(0, 0, Direction.NORTH, Command.L)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "ForwardMovementStrategy cannot handle" in str(e)


class TestTurnMovementStrategy:
    def test_execute_turn_left_from_north(self):
        strategy = TurnMovementStrategy()
        x, y, direction = strategy.execute(1, 1, Direction.NORTH, Command.L)
        assert x == 1
        assert y == 1
        assert direction == Direction.WEST

    def test_execute_turn_right_from_north(self):
        strategy = TurnMovementStrategy()
        x, y, direction = strategy.execute(1, 1, Direction.NORTH, Command.R)
        assert x == 1
        assert y == 1
        assert direction == Direction.EAST

    def test_execute_turn_left_from_east(self):
        strategy = TurnMovementStrategy()
        x, y, direction = strategy.execute(2, 2, Direction.EAST, Command.L)
        assert x == 2
        assert y == 2
        assert direction == Direction.NORTH

    def test_execute_turn_right_from_west(self):
        strategy = TurnMovementStrategy()
        x, y, direction = strategy.execute(0, 0, Direction.WEST, Command.R)
        assert x == 0
        assert y == 0
        assert direction == Direction.NORTH

    def test_execute_invalid_command_raises_error(self):
        strategy = TurnMovementStrategy()
        try:
            strategy.execute(0, 0, Direction.NORTH, Command.F)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "TurnMovementStrategy cannot handle" in str(e)
