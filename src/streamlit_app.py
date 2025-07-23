import io
import logging
import sys
import time
from contextlib import redirect_stderr, redirect_stdout

import streamlit as st

from application import Simulation
from constants import Direction
from domain import Grid


class OutputCapture:
    def __init__(self):
        self.content = []
    
    def write(self, text):
        if text.strip():
            self.content.append(text.strip())
    
    def flush(self):
        pass
    
    def get_content(self):
        return "\n".join(self.content)


class PrintCapture:
    def __init__(self):
        self.content = []
        self.current_line = ""
    
    def write(self, text):
        if text == "\n":
            if self.current_line.strip():
                self.content.append(self.current_line.strip())
            self.current_line = ""
        else:
            self.current_line += text
    
    def flush(self):
        if self.current_line.strip():
            self.content.append(self.current_line.strip())
            self.current_line = ""
    
    def get_content(self):
        self.flush()
        return "\n".join(self.content)
    
    def clear(self):
        self.content = []
        self.current_line = ""


def parse_direction(direction_str):
    direction_map = {
        "N": Direction.NORTH,
        "S": Direction.SOUTH,
        "E": Direction.EAST,
        "W": Direction.WEST,
    }
    return direction_map[direction_str.upper()]


def parse_input(input_text):
    lines = [line.strip() for line in input_text.split('\n')]
    
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    
    if not lines:
        raise ValueError("Empty input!")
    
    try:
        grid_parts = lines[0].split()
        if len(grid_parts) != 2:
            raise ValueError("Grid size must have exactly 2 numbers")
        grid_size_x, grid_size_y = map(int, grid_parts)
        if grid_size_x <= 0 or grid_size_y <= 0:
            raise ValueError("Grid dimensions must be positive")
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid grid size format: '{lines[0]}'. Expected: two positive integers (e.g., '10 10')")
    
    cars = []
    i = 1
    car_number = 1
    
    while i < len(lines):
        while i < len(lines) and not lines[i]:
            i += 1
        
        if i >= len(lines):
            break
        
        car_id = lines[i]
        if not car_id:
            raise ValueError(f"Car {car_number} has empty ID")
        i += 1
        
        if i >= len(lines):
            raise ValueError(f"Car {car_number} ('{car_id}') missing position and direction")
        
        try:
            pos_parts = lines[i].split()
            if len(pos_parts) != 3:
                raise ValueError("Position must have exactly 3 parts: x y direction")
            x, y, direction = int(pos_parts[0]), int(pos_parts[1]), pos_parts[2].upper()
            if x < 0 or y < 0:
                raise ValueError("Coordinates must be non-negative")
            if direction not in ["N", "S", "E", "W"]:
                raise ValueError("Direction must be N, S, E, or W")
        except (ValueError, IndexError) as e:
            raise ValueError(f"Car {car_number} ('{car_id}') has invalid position/direction: '{lines[i]}'. Expected format: 'x y direction' (e.g., '1 2 N')")
        
        position_direction = lines[i]
        i += 1
        
        commands = ""
        if i < len(lines) and lines[i]:
            is_next_car = (
                i + 1 < len(lines) and lines[i + 1] and len(lines[i + 1].split()) == 3
            )
            
            if not is_next_car:
                commands = lines[i]
                for cmd in commands:
                    if cmd not in "FLR":
                        raise ValueError(f"Car {car_number} ('{car_id}') has invalid command '{cmd}' in '{commands}'. Commands must contain only F (Forward), L (Left), R (Right)")
                i += 1
        
        cars.append([car_id, position_direction, commands])
        car_number += 1
    
    if not cars:
        raise ValueError("No cars found in input!")
    
    return grid_size_x, grid_size_y, cars


def visualize_grid(grid, step_info=""):
    max_dimension = max(grid.size_x, grid.size_y)
    if max_dimension <= 10:
        cell_size = 40
        font_size = 16
        index_font_size = 12
    elif max_dimension <= 15:
        cell_size = 30
        font_size = 14
        index_font_size = 10
    else:
        cell_size = 25
        font_size = 12
        index_font_size = 8
    
    container_width = (grid.size_x + 1) * cell_size + 40  # +1 for y-axis labels, +40 for padding
    
    grid_html = f"<div style='font-family: monospace; font-size: 14px; background-color: #1e1e1e; padding: 15px; border-radius: 8px; width: {container_width}px; overflow-x: auto;'>"
    
    if step_info:
        grid_html += f"<div style='margin-bottom: 15px; font-weight: bold; color: #ffffff; text-align: center;'>{step_info}</div>"
    
    grid_html += "<table style='border-collapse: collapse;'>"
    
    for y in range(grid.size_y - 1, -1, -1):
        grid_html += "<tr>"
        grid_html += f"<td style='width: {cell_size}px; height: {cell_size}px; text-align: center; color: #888; font-size: {index_font_size}px; font-weight: bold;'>{y}</td>"
        
        for x in range(grid.size_x):
            cell_content = "."
            cell_color = "#2d2d2d"
            text_color = "#666"
            
            for car_id, car in grid.cars.items():
                if car.x == x and car.y == y:
                    direction_arrows = {
                        Direction.NORTH: "↑",
                        Direction.SOUTH: "↓", 
                        Direction.EAST: "→",
                        Direction.WEST: "←"
                    }
                    arrow = direction_arrows.get(car.direction, "?")
                    cell_content = f"{car_id}{arrow}"
                    cell_color = "#ffd700"
                    text_color = "#000"
                    break
            
            grid_html += f"<td style='border: 1px solid #555; width: {cell_size}px; height: {cell_size}px; text-align: center; background-color: {cell_color}; color: {text_color}; font-size: {font_size}px; font-weight: bold;'>{cell_content}</td>"
        grid_html += "</tr>"
    
    index_height = max(20, cell_size * 0.75)
    grid_html += f"<tr><td style='width: {cell_size}px; height: {index_height}px;'></td>"
    for x in range(grid.size_x):
        grid_html += f"<td style='width: {cell_size}px; height: {index_height}px; text-align: center; color: #888; font-size: {index_font_size}px; font-weight: bold;'>{x}</td>"
    grid_html += "</tr>"
    
    grid_html += "</table></div>"
    return grid_html


def run_simulation_step_by_step(grid_size_x, grid_size_y, cars, output_capture, grid_placeholder, console_placeholder, print_capture, print_placeholder):
    try:
        print_capture.clear()
        
        with redirect_stdout(print_capture):
            simulation = Simulation(grid_size_x=grid_size_x, grid_size_y=grid_size_y, cars=cars)
        
        grid_html = visualize_grid(simulation.grid, "Initial State")
        grid_placeholder.markdown(grid_html, unsafe_allow_html=True)
        
        output_capture.write(f"Grid size: {grid_size_x}x{grid_size_y}")
        for car in cars:
            output_capture.write(f"Car data: {car}")
        output_capture.write("Starting simulation...")
        console_placeholder.code(output_capture.get_content(), language=None)
        
        time.sleep(0.5)
        
        collision_detected = False
        
        for step in range(simulation.max_step):
            output_capture.write(f"Step {step + 1}:")
            
            for car_id, car in simulation.grid.cars.items():
                current_command = car.get_next_command(simulation.grid.current_step)
                if current_command is not None:
                    output_capture.write(f"  Car {car_id} at ({car.x}, {car.y}) facing {car.direction.name} - executing command '{current_command}'")
                else:
                    output_capture.write(f"  Car {car_id} at ({car.x}, {car.y}) facing {car.direction.name} - no more commands")
            
            with redirect_stdout(print_capture):
                collision_result = simulation.grid.next_step()
                collision_detected = collision_result["collision"]
            
            output_capture.write("After step:")
            for car_id, car in simulation.grid.cars.items():
                output_capture.write(f"  Car {car_id} now at ({car.x}, {car.y}) facing {car.direction.name}")
            
            step_info = f"Step {step + 1}/{simulation.max_step}"
            if collision_detected:
                car_ids = ", ".join(collision_result["cars"])
                position = collision_result["position"]
                step_info += f" - COLLISION: Cars {car_ids} at ({position[0]}, {position[1]})"
            
            grid_html = visualize_grid(simulation.grid, step_info)
            grid_placeholder.markdown(grid_html, unsafe_allow_html=True)
            
            output_capture.write("-" * 40)
            console_placeholder.code(output_capture.get_content(), language=None)
            
            print_content = print_capture.get_content()
            if print_content:
                print_placeholder.code(print_content, language=None)
            else:
                print_placeholder.text("No print output yet...")
            
            if collision_detected:
                break
            
            time.sleep(0.5)
        
        if not collision_detected:
            with redirect_stdout(print_capture):
                output_capture.write("no collision")
                print("no collision")
            
            print_content = print_capture.get_content()
            if print_content:
                print_placeholder.code(print_content, language=None)
            else:
                print_placeholder.text("No print statements found.")
        
        output_capture.write("Simulation complete.")
        console_placeholder.code(output_capture.get_content(), language=None)
        
    except Exception as e:
        output_capture.write(f"ERROR: Simulation failed: {e}")
        console_placeholder.code(output_capture.get_content(), language=None)
        print_placeholder.text("Simulation failed - no print output.")


def main():
    st.set_page_config(page_title="Car Simulation", layout="wide")
    st.title("Auto-Driving Car Simulation")
    
    st.markdown("""
    <style>
    .main .block-container {
        max-width: 100%;
        padding-left: 1rem;
        padding-right: 1rem;
        padding-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1_top, col2_top = st.columns([2, 1])
    
    with col1_top:
        st.header("Simulation")
    
    with col2_top:
        st.header("Input")
    
    col1_content, col2_content = st.columns([2, 1])
    
    with col1_content:
        grid_placeholder = st.empty()
    
    with col2_content:
        input_text = st.text_area(
            "Enter simulation input:",
            height=400,
            placeholder="""15 15

A
1 2 N
FFRFFFFFRL

B
12 13 W
FFLFFFFFFF

C
5 4 S
FFFRFFFFLF
""",
            help="""Format:
Line 1: grid_size_x grid_size_y
Then for each car:
- Car ID (single character or string)
- Starting position: x y direction
- Commands (optional, can be empty line)
- Empty line between cars (optional)

Directions: N (North), S (South), E (East), W (West)
Commands: F (Forward), L (Left turn), R (Right turn)"""
        )
        
        run_button = st.button("Run Simulation", type="primary")
    
    col1_bottom, col2_bottom = st.columns([2, 1])
    
    with col1_bottom:
        st.header("Debug Output")
    
    with col2_bottom:
        st.header("Output")
    
    col1_debug, col2_output = st.columns([2, 1])
    
    with col1_debug:
        console_placeholder = st.empty()
    
    with col2_output:
        print_placeholder = st.empty()
    
    if 'output_capture' not in st.session_state:
        st.session_state.output_capture = OutputCapture()
    if 'print_capture' not in st.session_state:
        st.session_state.print_capture = PrintCapture()
    
    if run_button and input_text.strip():
        st.session_state.output_capture = OutputCapture()
        st.session_state.print_capture = PrintCapture()
        
        try:
            grid_size_x, grid_size_y, cars = parse_input(input_text)
            
            run_simulation_step_by_step(
                grid_size_x, grid_size_y, cars, 
                st.session_state.output_capture,
                grid_placeholder, 
                console_placeholder,
                st.session_state.print_capture,
                print_placeholder
            )
            
        except Exception as e:
            st.session_state.output_capture.write(f"ERROR: {e}")
            console_placeholder.code(st.session_state.output_capture.get_content(), language=None)
            grid_placeholder.error(f"Error: {e}")
            print_placeholder.text("Parsing failed - no print output.")
    
    elif run_button and not input_text.strip():
        grid_placeholder.warning("Please enter simulation input first!")


if __name__ == "__main__":
    main()
