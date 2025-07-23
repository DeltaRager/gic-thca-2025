from domain.car import Car
from domain.parser import SimpleCommandParser
from domain.movement_strategies import ForwardMovementStrategy, TurnMovementStrategy
from constants import Direction, Command

class TestCar:
    def test_car_creation_with_dependencies(self):
        parser = SimpleCommandParser()
        forward_strategy = ForwardMovementStrategy()
        turn_strategy = TurnMovementStrategy()
        
        car = Car(
            x=1, y=1, direction=Direction.NORTH,
            command_parser=parser,
            forward_strategy=forward_strategy,
            turn_strategy=turn_strategy
        )
        
        assert car.x == 1
        assert car.y == 1
        assert car.direction == Direction.NORTH
        assert car.position == (1, 1)
    
    def test_add_commands_uses_parser(self):
        parser = SimpleCommandParser()
        forward_strategy = ForwardMovementStrategy()
        turn_strategy = TurnMovementStrategy()
        
        car = Car(
            x=0, y=0, direction=Direction.NORTH,
            command_parser=parser,
            forward_strategy=forward_strategy,
            turn_strategy=turn_strategy
        )
        
        car.add_commands("FLR")

        assert len(car._commands) == 3
        assert car._commands == [Command.F, Command.L, Command.R]
    
    def test_move_forward_uses_strategy(self):
        parser = SimpleCommandParser()
        forward_strategy = ForwardMovementStrategy()
        turn_strategy = TurnMovementStrategy()
        
        car = Car(
            x=0, y=0, direction=Direction.NORTH,
            command_parser=parser,
            forward_strategy=forward_strategy,
            turn_strategy=turn_strategy
        )
        
        car.move(Command.F)
        assert car.x == 0
        assert car.y == 1
        assert car.direction == Direction.NORTH
    
    def test_move_turn_uses_strategy(self):
        parser = SimpleCommandParser()
        forward_strategy = ForwardMovementStrategy()
        turn_strategy = TurnMovementStrategy()
        
        car = Car(
            x=1, y=1, direction=Direction.NORTH,
            command_parser=parser,
            forward_strategy=forward_strategy,
            turn_strategy=turn_strategy
        )
        
        car.move(Command.L)
        assert car.x == 1
        assert car.y == 1
        assert car.direction == Direction.WEST
    
    def test_calculate_command_delegates_to_strategies(self):
        parser = SimpleCommandParser()
        forward_strategy = ForwardMovementStrategy()
        turn_strategy = TurnMovementStrategy()
        
        car = Car(
            x=2, y=2, direction=Direction.EAST,
            command_parser=parser,
            forward_strategy=forward_strategy,
            turn_strategy=turn_strategy
        )

        x, y, direction = car.calculate_command(Command.F)
        assert x == 3
        assert y == 2
        assert direction == Direction.EAST

        x, y, direction = car.calculate_command(Command.R)
        assert x == 2
        assert y == 2
        assert direction == Direction.SOUTH
