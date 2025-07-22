from src.domain import Car
from src.constants import Direction

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
