from src.domain import Grid
from src.settings import settings
from pydantic import ValidationError

class TestCar:
    def test_normal_grid_creation(self):
        grid_obj = Grid(
            size=10
        )

        assert grid_obj.size == 10
        assert len(grid_obj.cars) == 0

    def test_grid_creation_with_invalid_size(self):
        try:
            Grid(size=-1)
        except ValueError as e:
            assert any('Size must be a positive integer' in err['msg'] for err in e.errors())

        try:
            Grid(size=0)
        except ValueError as e:
            assert any('Size must be a positive integer' in err['msg'] for err in e.errors())

        try:
            Grid(size=1000)
        except ValueError as e:
            assert any(f'Size must not exceed MAX_GRID_SIZE={settings.max_grid_size}' in err['msg'] for err in e.errors())

    def test_grid_within_bounds(self):
        grid_obj = Grid(size=10)
        assert grid_obj.is_within_bounds(0, 0) is True
        assert grid_obj.is_within_bounds(9, 9) is True
        assert grid_obj.is_within_bounds(10, 10) is False
        assert grid_obj.is_within_bounds(-1, -1) is False
