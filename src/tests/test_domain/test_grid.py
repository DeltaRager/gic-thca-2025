from constants import Direction
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
            assert any(
                "Grid size_x must be a positive integer" in err["msg"]
                for err in e.errors()
            )

        try:
            Grid(size_x=10, size_y=0)
        except ValueError as e:
            assert any(
                "Grid size_y must be a positive integer" in err["msg"]
                for err in e.errors()
            )

        try:
            Grid(size_x=1000, size_y=10)
        except ValueError as e:
            assert any(
                f"Grid size_x cannot exceed {settings.max_grid_size_x}" in err["msg"]
                for err in e.errors()
            )

    def test_grid_within_bounds(self):
        grid_obj = Grid(size_x=10, size_y=10)
        assert grid_obj.is_within_bounds(0, 0) is True
        assert grid_obj.is_within_bounds(9, 9) is True
        assert grid_obj.is_within_bounds(10, 10) is False
        assert grid_obj.is_within_bounds(-1, -1) is False

    def test_add_car_capacity_limit(self):
        grid = Grid(size_x=2, size_y=2)

        grid.add_car("A", 0, 0, Direction.NORTH, "")
        grid.add_car("B", 0, 1, Direction.NORTH, "")
        grid.add_car("C", 1, 0, Direction.NORTH, "")
        grid.add_car("D", 1, 1, Direction.NORTH, "")

        try:
            grid.add_car("E", 0, 0, Direction.NORTH, "")
            assert False
        except ValueError as e:
            assert "Cannot add more cars than the grid can hold" in str(e)

    def test_add_car_position_occupied(self):
        grid = Grid(size_x=5, size_y=5)
        grid.add_car("A", 2, 2, Direction.NORTH, "")

        try:
            grid.add_car("B", 2, 2, Direction.SOUTH, "")
            assert False
        except ValueError as e:
            assert "Position (2, 2) is already occupied by car A" in str(e)

    def test_check_collisions_no_collisions(self):
        grid = Grid(size_x=5, size_y=5)
        grid.add_car("A", 1, 1, Direction.NORTH, "")
        grid.add_car("B", 2, 2, Direction.SOUTH, "")

        result = grid.check_collisions()
        assert result["collision"] == False

    def test_check_collisions_with_collision(self):
        grid = Grid(size_x=5, size_y=5)
        grid.add_car("A", 2, 2, Direction.NORTH, "")
        grid.add_car("B", 3, 3, Direction.WEST, "")

        grid.cars["A"].x = 2
        grid.cars["A"].y = 3
        grid.cars["B"].x = 2
        grid.cars["B"].y = 3

        result = grid.check_collisions()
        assert result["cars"] == ["A", "B"]
        assert result["collision"] == True
        assert result["position"] == (2, 3)

    def test_next_step_with_commands(self):
        grid = Grid(size_x=5, size_y=5)
        grid.add_car("A", 1, 1, Direction.NORTH, "F")

        initial_step = grid.current_step
        grid.next_step()

        assert grid.current_step == initial_step + 1
        assert grid.cars["A"].x == 1
        assert grid.cars["A"].y == 2

    def test_next_step_out_of_bounds(self):
        grid = Grid(size_x=2, size_y=2)
        grid.add_car("A", 1, 1, Direction.NORTH, "F")

        grid.next_step()

        assert grid.cars["A"].x == 1
        assert grid.cars["A"].y == 1

    def test_next_step_no_commands(self):
        grid = Grid(size_x=5, size_y=5)
        grid.add_car("A", 1, 1, Direction.NORTH, "")

        initial_pos = (grid.cars["A"].x, grid.cars["A"].y)
        grid.next_step()

        assert (grid.cars["A"].x, grid.cars["A"].y) == initial_pos

    def test_is_within_bounds_valid(self):
        grid = Grid(size_x=10, size_y=8)

        assert grid.is_within_bounds(0, 0) == True
        assert grid.is_within_bounds(9, 7) == True
        assert grid.is_within_bounds(5, 4) == True

    def test_is_within_bounds_invalid(self):
        grid = Grid(size_x=10, size_y=8)

        assert grid.is_within_bounds(-1, 0) == False
        assert grid.is_within_bounds(0, -1) == False
        assert grid.is_within_bounds(10, 0) == False
        assert grid.is_within_bounds(0, 8) == False
        assert grid.is_within_bounds(10, 8) == False

    def test_remove_car_existing(self):
        grid = Grid(size_x=5, size_y=5)
        grid.add_car("A", 1, 1, Direction.NORTH, "")

        assert "A" in grid.cars
        grid.remove_car("A")
        assert "A" not in grid.cars

    def test_remove_car_nonexistent(self):
        grid = Grid(size_x=5, size_y=5)

        try:
            grid.remove_car("X")
            assert False
        except ValueError as e:
            assert "Car with id 'X' does not exist" in str(e)
