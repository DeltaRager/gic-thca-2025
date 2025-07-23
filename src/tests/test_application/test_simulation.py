from application.simulation import Simulation, parse_direction
from constants import Direction


class TestParseDirection:
    def test_parse_north(self):
        result = parse_direction("N")
        assert result == Direction.NORTH

    def test_parse_south(self):
        result = parse_direction("S")
        assert result == Direction.SOUTH

    def test_parse_east(self):
        result = parse_direction("E")
        assert result == Direction.EAST

    def test_parse_west(self):
        result = parse_direction("W")
        assert result == Direction.WEST

    def test_parse_lowercase(self):
        result = parse_direction("n")
        assert result == Direction.NORTH

    def test_parse_invalid_direction(self):
        try:
            parse_direction("X")
            assert False
        except KeyError:
            assert True


class TestSimulation:
    def test_simulation_creation_single_car(self):
        cars = [["A", "1 2 N", "FFR"]]
        simulation = Simulation(10, 10, cars)
        assert simulation.grid.size_x == 10
        assert simulation.grid.size_y == 10
        assert len(simulation.grid.cars) == 1
        assert "A" in simulation.grid.cars

    def test_simulation_creation_multiple_cars(self):
        cars = [["A", "1 2 N", "FFR"], ["B", "5 5 S", "LLF"], ["C", "8 8 E", ""]]
        simulation = Simulation(10, 10, cars)
        assert len(simulation.grid.cars) == 3
        assert all(car_id in simulation.grid.cars for car_id in ["A", "B", "C"])

    def test_simulation_max_step_calculation(self):
        cars = [["A", "1 2 N", "FFR"], ["B", "5 5 S", "LLFRFRF"], ["C", "8 8 E", "F"]]
        simulation = Simulation(10, 10, cars)
        assert simulation.max_step == 7

    def test_simulation_empty_commands(self):
        cars = [["A", "1 2 N", ""]]
        simulation = Simulation(10, 10, cars)
        assert simulation.max_step == 0

    def test_simulation_mixed_command_lengths(self):
        cars = [["A", "1 2 N", "F"], ["B", "5 5 S", ""], ["C", "8 8 E", "FFRFRF"]]
        simulation = Simulation(10, 10, cars)
        assert simulation.max_step == 6
