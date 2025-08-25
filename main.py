# main.py
from graph_model import create_graph_from_grid, Cell
from dfs_solver import find_path_recursive, dfs_iterative

if __name__ == "__main__":
    # Define your maze
    rows = 5
    cols = 5
    start_pos_coords = (0, 0)
    goal_pos_coords = (4, 4)
    obstacles_coords = [(1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 1)]

    # Convert coordinates to Cell objects for consistent graph representation
    start_node = Cell(*start_pos_coords)
    goal_node = Cell(*goal_pos_coords)
    obstacles_nodes = [Cell(*o) for o in obstacles_coords]

    # Create the graph
    print("Creating graph...")
    # CORRECTED CALL: Only pass grid_dims and obstacles_nodes
    maze_graph = create_graph_from_grid((rows, cols), obstacles_nodes)
    print("Graph created.")

    # --- Test Recursive DFS ---
    print("\n--- Running Recursive DFS ---")
    recursive_path = find_path_recursive(maze_graph, start_node, goal_node)
    if recursive_path:
        print("Recursive DFS Path Found:")
        # Convert Cell objects in path to string for cleaner output
        print([str(node) for node in recursive_path])
    else:
        print("No path found by Recursive DFS.")

    # --- Test Iterative DFS ---
    print("\n--- Running Iterative DFS ---")
    iterative_path = dfs_iterative(maze_graph, start_node, goal_node)
    if iterative_path:
        print("Iterative DFS Path Found:")
        # Convert Cell objects in path to string for cleaner output
        print([str(node) for node in iterative_path])
    else:
        print("No path found by Iterative DFS.")

    # You would expand this main.py for more complex scenarios,
    # and integrate with visualization in Chapter 3.
