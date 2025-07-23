# Auto Driving Car Simulation - GIC 2025

An auto-driving car simulation project that models car movement on a grid with collision detection. The project implements clean architecture patterns with a domain-driven design approach.

## Features

- Grid-based car simulation with configurable dimensions (up to 20x20)
- Car movement with directional commands (Forward, Left turn, Right turn)
- Real-time collision detection
- Step-by-step visualization via Streamlit web interface
- Command-line interface for batch processing
- Comprehensive test suite with TDD approach
- Clean architecture with separated layers

## Project Structure

```
src/
├── domain/                 # Core business logic
│   ├── car.py             # Car entity with movement logic
│   ├── grid.py            # Grid management and simulation
│   ├── interfaces.py      # Abstract interfaces
│   ├── movement_strategies.py  # Movement strategy implementations
│   └── parser.py          # Command parsing logic
├── application/           # Use cases and orchestration
│   └── simulation.py      # Main simulation coordinator
├── constants/             # Enums and mappings
│   ├── commands.py        # Command definitions
│   └── directions.py      # Direction vectors and mappings
├── tests/                 # Test suite mirroring source structure
├── main.py               # CLI entry point
├── streamlit_app.py      # Web UI application
├── settings.py           # Configuration management
└── settings.toml         # Configuration file
```

## Prerequisites

- Python 3.12
- Git

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/DeltaRager/gic-thca-2025.git
cd gic-thca-2025
```

### 2. Create Virtual Environment

```bash
python -m venv gic_venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
gic_venv\Scripts\activate
```

**macOS/Linux:**
```bash
source gic_venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

### Web Interface (Streamlit)

Launch the interactive web interface:

```bash
streamlit run src/streamlit_app.py
```

The application will open in your browser at `http://localhost:8501`

#### Web Interface Features:
- **Simulation**: Visual grid with step-by-step car movement
- **Input**: Text area for simulation configuration
- **Debug Output**: Detailed step information and car states
- **Output**: Print statements from collision detection
- **Dynamic Grid**: Automatically scales from 10x10 to 20x20
- **Dark Theme**: Professional appearance with directional arrows

### Command Line Interface

Run simulations via command line:

```bash
PYTHONPATH=src python src/main.py input.txt
```

Or use the provided script:

```bash
./scripts/run_app.sh
```

## Input Format

The simulation accepts input in the following format (in input.txt):

```
grid_size_x grid_size_y

car_id
x y direction
commands

car_id
x y direction
commands
```

### Example Input:

```
10 10

A
1 2 N
FFRFFFRRLF

B
7 8 W
FFLFFFFFFF

C
5 4 S
```

### Input Rules:
- **Grid Size**: Two positive integers (max 20x20)
- **Car ID**: Single character or string identifier
- **Position**: x y coordinates (non-negative integers starting from 0)
- **Direction**: N (North), S (South), E (East), W (West)
- **Commands**: F (Forward), L (Left turn), R (Right turn)
- **Empty Lines**: Optional between cars


### Command Rules:
- **L**: Rotates the car by 90 degrees to the left
- **R**: Rotates the car by 90 degrees to the right
- **F**: Moves forward by 1 grid point

## Running Tests

### Run All Tests

```bash
PYTHONPATH=src python -m pytest
```

Or use the provided script:

```bash
./scripts/run_test.sh
```

### Run Specific Tests

```bash
PYTHONPATH=src python -m pytest src/tests/test_domain/test_car.py
```

### Run Tests with Coverage

```bash
PYTHONPATH=src python -m pytest --cov=src --cov-report=html
```

### Test Structure

The test suite follows the same structure as the source code:
- `test_domain/`: Tests for core business logic
- `test_application/`: Tests for use cases
- `test_main.py`: Integration tests

## Development Workflow

### 1. Test-Driven Development (TDD)

Always write tests first:

```bash
# Write failing test
PYTHONPATH=src python -m pytest src/tests/test_domain/test_car.py::TestCar::test_new_feature

# Implement minimal code to pass
# Run tests again to verify
```

### 2. Code Quality

Run code formatting and linting:

```bash
black src/
isort src/
```

### 3. Pre-commit Hooks

Install pre-commit hooks for automatic code quality checks:

```bash
pre-commit install
```

## Configuration

Application settings are managed in `src/settings.toml`:

```toml
max_grid_size_x = 20
max_grid_size_y = 20
log_level = "critical"
```

## Architecture Principles

### Clean Architecture Layers:
1. **Domain Layer**: Pure business logic, no external dependencies
2. **Application Layer**: Use cases that orchestrate domain objects
3. **Infrastructure**: External concerns (settings, I/O)

## Collision Detection

The simulation detects collisions when:
- Multiple cars occupy the same grid position
- Collision information includes car IDs and position coordinates
- Simulation stops immediately upon collision detection

## Output Formats

### Success (No Collision):
```
no collision
```

### Collision Detected:
```
A B C
5 4
7
```
Where:
- Line 1: Colliding car IDs
- Line 2: Collision position (x y)
- Line 3: Step number when collision occurred

## Troubleshooting

### Common Issues:

1. **Import Errors**: Ensure `PYTHONPATH=src` is set
2. **Test Failures**: Check that virtual environment is activated
3. **Streamlit Issues**: Verify streamlit is installed and port 8501 is free
4. **Permission Errors**: Ensure scripts have execute permissions

### Debug Mode:

Change log level in `settings.toml`:
```toml
log_level = "debug"
```

## AI Usage

This project was developed using claude code. The parts that were written by AI are as follows:

- Documentation
- Tests after providing an example type for a test
- Help fixing complex multi file errors
- Help check whether SOLID principles or Clean architecture was majorily violated
