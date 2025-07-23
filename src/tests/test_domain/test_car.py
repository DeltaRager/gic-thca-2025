from src.domain import Car
from src.constants import Direction, Command

class TestCar:
    def test_normal_car_creation(self):
        car_obj = Car(
            x=0,
            y=0,
            direction=Direction.NORTH,
        )

        assert car_obj.x == 0
        assert car_obj.y == 0
        assert car_obj.position == (0, 0)
        assert car_obj.direction == Direction.NORTH

    def test_car_creation_with_negative_coordinates(self):
        try:
            Car(x=-1, y=0, direction=Direction.EAST)
        except ValueError as e:
            assert any('Coordinates must be non-negative' in err['msg'] for err in e.errors())

        try:
            Car(x=0, y=-1, direction=Direction.SOUTH)
        except ValueError as e:
            assert any('Coordinates must be non-negative' in err['msg'] for err in e.errors())

        try:
            Car(x=-1, y=-1, direction=Direction.SOUTH)
        except ValueError as e:
            assert any('Coordinates must be non-negative' in err['msg'] for err in e.errors())

    def test_car_creation_with_invalid_direction(self):
        try:
            Car(x=0, y=0, direction='INVALID_DIRECTION')
        except ValueError as e:
            print(e.errors())
            assert any('Input should be (0, 1), (0, -1), (1, 0) or (-1, 0)' in err['msg'] for err in e.errors())

        try:
            Car(x=1, y=1, direction=None)
        except ValueError as e:
            assert any('Input should be (0, 1), (0, -1), (1, 0) or (-1, 0)' in err['msg'] for err in e.errors())

    def test_car_calculate_command(self):
        car_obj = Car(x=0, y=0, direction=Direction.NORTH)

        x,y,_ = car_obj.calculate_command(Command.F)
        assert (x, y) == (0, 1)

        _,_,direction = car_obj.calculate_command(Command.L)
        assert direction == Direction.WEST

        _,_,direction = car_obj.calculate_command(Command.R)
        assert direction == Direction.EAST

        car_obj.direction = direction
        _,_,direction = car_obj.calculate_command(Command.R)
        assert direction == Direction.SOUTH

        car_obj.direction = direction
        _,_,direction = car_obj.calculate_command(Command.R)
        assert direction == Direction.WEST

        try:
            car_obj.calculate_command('INVALID_COMMAND')
        except ValueError as e:
            assert True
    
