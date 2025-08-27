import time
import tracemalloc
import sys
import random
import numpy as np
import matplotlib.pyplot as plt
from graph_model import Cell, create_graph_from_grid
from dfs_solver import find_path_recursive, dfs_iterative

# Analysis Configuration
GRID_SIZES = [(20, 20), (40, 40), (60, 60)]
OBSTACLE_DENSITIES = [0.1, 0.2, 0.3] # 10%, 20%, 30%
NUM_RUNS = 3  # Number of runs to average

def generate_obstacles(grid_size, density):
    rows, cols = grid_size
    obstacles = set()
    num_obstacles = int(rows * cols * density)
    while len(obstacles) < num_obstacles:
        r, c = random.randint(0, rows - 1), random.randint(0, cols - 1)
        # Ensure start and goal are not obstacles
        if (r, c) != (0, 0) and (r, c) != (rows - 1, cols - 1):
            obstacles.add(Cell(r, c))
    return list(obstacles)

def run_single_analysis(grid_size, obstacle_density, algorithm):
    rows, cols = grid_size
    graph = create_graph_from_grid(grid_size, generate_obstacles(grid_size, obstacle_density))
    start_node = Cell(0, 0)
    goal_node = Cell(rows - 1, cols - 1)

    # Set a higher recursion limit for larger grids for the recursive algorithm
    if algorithm == 'recursive':
        original_limit = sys.getrecursionlimit()
        new_limit = rows * cols
        if new_limit > original_limit:
            sys.setrecursionlimit(new_limit)

    tracemalloc.start()
    start_time = time.perf_counter()

    if algorithm == 'recursive':
        path, _, max_depth = find_path_recursive(graph, start_node, goal_node)
    else:
        path, _ = dfs_iterative(graph, start_node, goal_node)
        max_depth = 0 # Not applicable for iterative

    end_time = time.perf_counter()
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if algorithm == 'recursive':
        sys.setrecursionlimit(original_limit) # Reset to default

    return {
        'time': end_time - start_time,
        'memory': peak_mem / 1024,  # in KB
        'depth': max_depth,
        'path_found': path is not None
    }

def main():
    results = {size: {density: {'recursive': [], 'iterative': []} for density in OBSTACLE_DENSITIES} for size in GRID_SIZES}

    print("Running performance analysis...")
    for size in GRID_SIZES:
        for density in OBSTACLE_DENSITIES:
            print(f"  Grid Size: {size}, Obstacle Density: {density*100}%")
            for _ in range(NUM_RUNS):
                results[size][density]['recursive'].append(run_single_analysis(size, density, 'recursive'))
                results[size][density]['iterative'].append(run_single_analysis(size, density, 'iterative'))
    print("Analysis complete.")

    # --- Data Processing and Plotting ---

    # 1. Execution Time Plot
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    bar_width = 0.2
    for i, density in enumerate(OBSTACLE_DENSITIES):
        rec_times = [np.mean([run['time'] for run in results[size][density]['recursive']]) for size in GRID_SIZES]
        it_times = [np.mean([run['time'] for run in results[size][density]['iterative']]) for size in GRID_SIZES]
        
        r = np.arange(len(GRID_SIZES))
        ax1.bar(r - bar_width/2 + i*bar_width, rec_times, width=bar_width, label=f'Recursive {density*100}%')
        ax1.bar(r + bar_width/2 + i*bar_width, it_times, width=bar_width, label=f'Iterative {density*100}%')

    ax1.set_title('Execution Time vs. Grid Size')
    ax1.set_ylabel('Time (seconds)')
    ax1.set_xticks([r + bar_width for r in range(len(GRID_SIZES))])
    ax1.set_xticklabels([f'{s[0]}x{s[1]}' for s in GRID_SIZES])
    ax1.legend()
    fig1.savefig('execution_time_analysis.png')
    print("Execution time analysis saved to execution_time_analysis.png")

    # 2. Memory Usage Plot
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    for i, density in enumerate(OBSTACLE_DENSITIES):
        rec_mems = [np.mean([run['memory'] for run in results[size][density]['recursive']]) for size in GRID_SIZES]
        it_mems = [np.mean([run['memory'] for run in results[size][density]['iterative']]) for size in GRID_SIZES]

        r = np.arange(len(GRID_SIZES))
        ax2.bar(r - bar_width/2 + i*bar_width, rec_mems, width=bar_width, label=f'Recursive {density*100}%')
        ax2.bar(r + bar_width/2 + i*bar_width, it_mems, width=bar_width, label=f'Iterative {density*100}%')

    ax2.set_title('Peak Memory Usage vs. Grid Size')
    ax2.set_ylabel('Memory (KB)')
    ax2.set_xticks([r + bar_width for r in range(len(GRID_SIZES))])
    ax2.set_xticklabels([f'{s[0]}x{s[1]}' for s in GRID_SIZES])
    ax2.legend()
    fig2.savefig('memory_usage_analysis.png')
    print("Memory usage analysis saved to memory_usage_analysis.png")

    # 3. Stack Depth Plot
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    for i, density in enumerate(OBSTACLE_DENSITIES):
        depths = [np.mean([run['depth'] for run in results[size][density]['recursive']]) for size in GRID_SIZES]
        ax3.plot([f'{s[0]}x{s[1]}' for s in GRID_SIZES], depths, marker='o', linestyle='-', label=f'Density {density*100}%')

    ax3.set_title('Max Recursion Depth vs. Grid Size (Recursive DFS)')
    ax3.set_ylabel('Stack Depth')
    ax3.set_xlabel('Grid Size')
    ax3.legend()
    fig3.savefig('stack_depth_analysis.png')
    print("Stack depth analysis saved to stack_depth_analysis.png")

if __name__ == '__main__':
    main()
