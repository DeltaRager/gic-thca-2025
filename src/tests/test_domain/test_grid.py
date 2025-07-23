from domain import Grid
from settings import settings

class TestCar:
    def test_normal_grid_creation(self):
        grid_obj = Grid(
            size_x=10,
            size_y=10,
        )

        assert grid_obj.size_x == 10
        assert grid_obj.size_y == 10
        assert len(grid_obj.cars) == 0

    def test_grid_creation_with_invalid_size(self):
        try:
            Grid(size_x=-1, size_y=10)
        except ValueError as e:
            assert any('Grid size_x must be a positive integer' in err['msg'] for err in e.errors())

        try:
            Grid(size_x=10, size_y=0)
        except ValueError as e:
            assert any('Grid size_y must be a positive integer' in err['msg'] for err in e.errors())

        try:
            Grid(size_x=1000, size_y=10)
        except ValueError as e:
            assert any(f'Grid size_x cannot exceed {settings.max_grid_size_x}' in err['msg'] for err in e.errors())

    def test_grid_within_bounds(self):
        grid_obj = Grid(size_x=10, size_y=10)
        assert grid_obj.is_within_bounds(0, 0) is True
        assert grid_obj.is_within_bounds(9, 9) is True
        assert grid_obj.is_within_bounds(10, 10) is False
        assert grid_obj.is_within_bounds(-1, -1) is False
