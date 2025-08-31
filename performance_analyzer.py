# performance_analyzer.py

import time
import tracemalloc
import numpy as np
import random
import sys
from statistics import mean, stdev

# Project-specific imports
from graph_model import Cell, create_graph_from_grid
from dfs_solver import find_path_recursive, dfs_iterative

def run_performance_test(grid_size, density, algorithm, num_runs=5):
    """
    Runs a performance test for a given DFS algorithm on a grid of specific
    size and obstacle density.

    :param grid_size: A tuple (rows, cols) for the grid dimensions.
    :param density: The ratio of obstacles to total cells (0.0 to 1.0).
    :param algorithm: A string, either 'recursive' or 'iterative'.
    :param num_runs: The number of times to run the test to get an average.
    :return: A dictionary containing the average metrics.
    """
    rows, cols = grid_size
    start_node = Cell(0, 0)
    goal_node = Cell(rows - 1, cols - 1)

    times, memories, recursion_depths = [], [], []

    print(f"Testing {algorithm} DFS on {rows}x{cols} grid with {density*100:.0f}% density...")

    for i in range(num_runs):
        # Generate a new random grid for each run
        num_obstacles = int(rows * cols * density)
        obstacles = set()
        while len(obstacles) < num_obstacles:
            r, c = random.randint(0, rows - 1), random.randint(0, cols - 1)
            # Ensure start and goal are not obstacles
            if (r, c) != (start_node.row, start_node.col) and (r, c) != (goal_node.row, goal_node.col):
                obstacles.add(Cell(r, c))

        maze_graph = create_graph_from_grid(grid_size, list(obstacles))

        # Start measurements
        tracemalloc.start()
        start_time = time.perf_counter()

        path = None
        recursion_depth = 0

        if algorithm == 'recursive':
            # The third return value is the max_depth integer
            path, _, max_depth = find_path_recursive(maze_graph, start_node, goal_node)
            recursion_depth = max_depth
        else: # iterative
            path, _ = dfs_iterative(maze_graph, start_node, goal_node)
            recursion_depth = 0 # Not applicable for iterative

        end_time = time.perf_counter()
        _, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # If a path was found, store the results
        if path:
            times.append(end_time - start_time)
            memories.append(peak_mem / 1024)  # Convert to KB
            recursion_depths.append(recursion_depth)
        else:
            # If no path is found, the trial is invalid for performance timing
            # but we print a note. A real-world scenario might handle this differently.
            print(f"  - Run {i+1}/{num_runs}: No path found. Discarding result.")


    # Calculate averages, handling cases where no paths were found
    if not times:
        return {
            'avg_time': float('inf'),
            'avg_memory_kb': float('inf'),
            'avg_recursion_depth': float('inf'),
            'std_time': 0,
            'path_found_ratio': 0
        }

    return {
        'avg_time': mean(times),
        'avg_memory_kb': mean(memories),
        'avg_recursion_depth': mean(recursion_depths) if algorithm == 'recursive' else 0,
        'std_time': stdev(times) if len(times) > 1 else 0,
        'path_found_ratio': len(times) / num_runs
    }

def main():
    """
    Main function to define test parameters, run all tests, and print results.
    """
    # Increase Python's recursion limit to handle deep paths in large grids.
    # The max grid size is 60x60 = 3600 cells. A limit of 4000 is safe.
    sys.setrecursionlimit(4000)

    grid_sizes = [20, 40, 60]
    densities = [0.1, 0.2, 0.3]
    algorithms = ['recursive', 'iterative']

    # Store results in a nested dictionary: results[size][density][algo]
    results = {size: {f"{int(d*100)}%": {} for d in densities} for size in grid_sizes}

    for size in grid_sizes:
        for density in densities:
            for algo in algorithms:
                metrics = run_performance_test((size, size), density, algo)
                results[size][f"{int(density*100)}%"][algo] = metrics

    print("\n" + "="*80)
    print("PERFORMANCE ANALYSIS RESULTS")
    print("="*80 + "\n")

    # --- TABLE 1: Max Recursion Depth ---
    print("-" * 80)
    print("TABLE 1: Average Max Recursion Depth (Recursive DFS)")
    print("-" * 80)
    header = f"{ 'Grid Size':<15} | { '10% Density':<20} | { '20% Density':<20} | { '30% Density':<20}"
    print(header)
    print("-" * len(header))
    for size in grid_sizes:
        row = f"{ f'{size}x{size}':<15} | "
        for d_key in ['10%', '20%', '30%']:
            depth = results[size][d_key]['recursive']['avg_recursion_depth']
            row += f"{ f'{depth:.2f}':<20} | "
        print(row)

    # --- TABLE 2: Execution Time ---
    print("\n" + "-" * 80)
    print("TABLE 2: Average Execution Time (seconds)")
    print("-" * 80)
    header = f"{ 'Grid Size':<15} | { 'Algorithm':<12} | { '10% Density':<20} | { '20% Density':<20} | { '30% Density':<20}"
    print(header)
    print("-" * len(header))
    for size in grid_sizes:
        for algo in algorithms:
            row = f"{ f'{size}x{size}':<15} | {algo:<12} | "
            for d_key in ['10%', '20%', '30%']:
                time_val = results[size][d_key][algo]['avg_time']
                row += f"{ f'{time_val:.4f}s':<20} | "
            print(row)
        if size != grid_sizes[-1]:
            print("-" * len(header))


    # --- TABLE 3: Peak Memory Usage ---
    print("\n" + "-" * 80)
    print("TABLE 3: Average Peak Memory Usage (KB)")
    print("-" * 80)
    header = f"{ 'Grid Size':<15} | { 'Algorithm':<12} | { '10% Density':<20} | { '20% Density':<20} | { '30% Density':<20}"
    print(header)
    print("-" * len(header))
    for size in grid_sizes:
        for algo in algorithms:
            row = f"{ f'{size}x{size}':<15} | {algo:<12} | "
            for d_key in ['10%', '20%', '30%']:
                mem_val = results[size][d_key][algo]['avg_memory_kb']
                row += f"{ f'{mem_val:.2f} KB':<20} | "
            print(row)
        if size != grid_sizes[-1]:
            print("-" * len(header))

    print("\n" + "="*80)


if __name__ == '__main__':
    main()
