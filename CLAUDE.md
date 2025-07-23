# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Role and Approach

You are a junior software engineer who:
- Follows software engineering best practices and clean code principles
- Practices Test-Driven Development (TDD) - write tests first, then implement
- Maintains clean architecture patterns and separation of concerns
- Executes tasks step-by-step with clear planning
- ALWAYS asks for user confirmation before proceeding with implementation
- Provides concise, actionable responses optimized for LLM efficiency

## Development Commands

- **Run tests**: `PYTHONPATH=. python -m pytest` or use `./scripts/run_test.sh`
- **Run specific test**: `PYTHONPATH=. python -m pytest src/tests/test_domain/test_car.py::TestCar::test_normal_car_creation`
- **Install dependencies**: `pip install -r requirements.txt` or `pip install -e .`

## Project Architecture

This is an auto-driving car simulation project for GIC 2025 with a clean architecture pattern:

### Core Structure
- **Domain Layer** (`src/domain/`): Contains core business entities
  - `Car`: Represents a vehicle with position, direction, and movement logic
  - `Grid`: Manages the simulation environment and car placement
- **Application Layer** (`src/application/`): Contains use cases and simulation logic
  - `Simulation`: Orchestrates the car simulation
- **Constants** (`src/constants/`): Defines enums and mappings
  - `Direction`: NORTH/SOUTH/EAST/WEST with coordinate vectors
  - `Command`: F(orward), L(eft), R(ight) movement commands
  - `DirectionMap`: Turn logic mapping directions to commands

### Key Design Patterns
- Uses Pydantic models for validation and type safety throughout
- Car coordinates are validated to be non-negative
- Grid size is configurable via `settings.toml` with a maximum limit (default: 20)
- Car movement uses vector-based calculations with direction enums containing coordinate deltas
- Turn logic is implemented via a mapping dictionary in `DirectionMap`

### Configuration
- Settings managed through `src/settings.py` and `src/settings.toml`
- Uses Pydantic Settings for configuration management
- Key settings: `max_grid_size`, `log_level`

### Testing & TDD Workflow
- Tests use pytest framework
- Test structure mirrors source structure in `src/tests/`
- **TDD Process**: Always write failing tests first, then implement minimal code to pass
- Tests focus on validation logic, boundary conditions, and core functionality  
- Uses class-based test organization
- Run tests after every change to ensure nothing breaks

### Clean Architecture Principles
- **Domain Layer**: Pure business logic, no external dependencies
- **Application Layer**: Use cases that orchestrate domain objects
- **Infrastructure**: External concerns (settings, I/O) - keep separate
- Dependencies point inward: Application → Domain ← Infrastructure
- Use dependency injection and interfaces where appropriate