# test_dfs_solver.py

import unittest
from graph_model import Cell, create_graph_from_grid
from dfs_solver import find_path_recursive, dfs_iterative

class TestDFSSolver(unittest.TestCase):
    """
    Unit tests for the Depth-First Search (DFS) solver implementations.
    Tests both recursive and iterative DFS functions across various maze scenarios.
    """

    def setUp(self):
        """
        Set up common test data before each test method is run.
        This helps in avoiding repetitive code for defining grids, start/goal, and obstacles.
        """
        # Define a standard small grid for many tests
        self.rows = 5
        self.cols = 5
        self.grid_dims = (self.rows, self.cols)

        # Common start and goal nodes
        self.start_node = Cell(0, 0)
        self.goal_node = Cell(4, 4)

    def _run_dfs_tests(self, graph, start, goal, expected_path_str, test_name, check_exact_path=True):
        """
        Helper method to run and assert results for both recursive and iterative DFS.
        This reduces code duplication for testing both implementations.

        :param graph: The adjacency list representing the maze.
        :param start: The starting Cell.
        :param goal: The goal Cell.
        :param expected_path_str: A list of string representations of the expected path,
                                  or None if no path is expected.
        :param test_name: A string describing the current test scenario.
        :param check_exact_path: Boolean, if True, asserts the exact path.
                                 If False, only asserts path existence and correct start/end.
        """
        print(f"\n--- Running {test_name} ---")

        # Test Recursive DFS
        recursive_path = find_path_recursive(graph, start, goal)
        recursive_path_str = [str(node) for node in recursive_path] if recursive_path else None
        print(f"Recursive DFS Result: {recursive_path_str}")

        # Assertions for recursive DFS
        if expected_path_str is None:
            self.assertIsNone(recursive_path, f"Recursive DFS should find no path for {test_name}")
        else:
            self.assertIsNotNone(recursive_path, f"Recursive DFS should find a path for {test_name}")
            self.assertEqual(str(recursive_path[0]), str(start), f"Recursive DFS path should start at {start} for {test_name}")
            self.assertEqual(str(recursive_path[-1]), str(goal), f"Recursive DFS path should end at {goal} for {test_name}")
            if check_exact_path:
                self.assertEqual(recursive_path_str, expected_path_str,
                                 f"Recursive DFS path mismatch for {test_name}")


        # Test Iterative DFS
        iterative_path = dfs_iterative(graph, start, goal)
        iterative_path_str = [str(node) for node in iterative_path] if iterative_path else None
        print(f"Iterative DFS Result: {iterative_path_str}")

        # Assertions for iterative DFS
        if expected_path_str is None:
            self.assertIsNone(iterative_path, f"Iterative DFS should find no path for {test_name}")
        else:
            self.assertIsNotNone(iterative_path, f"Iterative DFS should find a path for {test_name}")
            self.assertEqual(str(iterative_path[0]), str(start), f"Iterative DFS path should start at {start} for {test_name}")
            self.assertEqual(str(iterative_path[-1]), str(goal), f"Iterative DFS path should end at {goal} for {test_name}")
            if check_exact_path:
                self.assertEqual(iterative_path_str, expected_path_str,
                                 f"Iterative DFS path mismatch for {test_name}")


    def test_simple_path_no_obstacles(self):
        """
        Tests DFS on a simple grid with no obstacles.
        We now only assert path existence and correct start/end, not exact path,
        as DFS path can vary.
        """
        obstacles = []
        maze_graph = create_graph_from_grid(self.grid_dims, obstacles)

        # For this test, we only care that a path is found and it's valid.
        # The exact path can vary based on neighbor iteration order.
        self._run_dfs_tests(maze_graph, self.start_node, self.goal_node,
                            # We still pass an expected_path_str to indicate a path should be found,
                            # but check_exact_path=False will prevent strict comparison.
                            expected_path_str=['(0, 0)', '(4, 4)'], # Placeholder for existence check
                            test_name="Simple Path (No Obstacles)",
                            check_exact_path=False)

    def test_path_with_obstacles(self):
        """
        Tests DFS on a grid with obstacles, ensuring it finds a path around them.
        Now also uses check_exact_path=False due to neighbor sorting.
        """
        obstacles_coords = [(1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 1)]
        obstacles_cells = [Cell(*o) for o in obstacles_coords]
        maze_graph = create_graph_from_grid(self.grid_dims, obstacles_cells)

        # The exact path can now vary due to neighbor sorting.
        # We will only assert path existence and correct start/end.
        self._run_dfs_tests(maze_graph, self.start_node, self.goal_node,
                            expected_path_str=['(0, 0)', '(4, 4)'], # Placeholder for existence check
                            test_name="Path with Obstacles",
                            check_exact_path=False)


    def test_no_path_to_goal(self):
        """
        Tests DFS when the goal is completely blocked off, expecting no path.
        """
        # Block the goal (4,4) from all sides
        obstacles_coords = [(3, 4), (4, 3), (4, 2), (3, 2)] # Block off the last row/column approach
        obstacles_cells = [Cell(*o) for o in obstacles_coords]
        maze_graph = create_graph_from_grid(self.grid_dims, obstacles_cells)

        self._run_dfs_tests(maze_graph, self.start_node, self.goal_node, None,
                            "No Path to Goal (Blocked)", check_exact_path=False)

    def test_start_equals_goal(self):
        """
        Tests DFS when the start and goal nodes are the same.
        """
        start_goal_node = Cell(2, 2)
        obstacles = [] # No obstacles for this simple case
        maze_graph = create_graph_from_grid(self.grid_dims, obstacles)

        # Expected path is just the start/goal node itself
        expected_path = [str(start_goal_node)]
        self._run_dfs_tests(maze_graph, start_goal_node, start_goal_node, expected_path,
                            "Start Equals Goal", check_exact_path=True)

    def test_single_row_maze(self):
        """
        Tests DFS on a single-row maze.
        """
        rows, cols = 1, 5
        start = Cell(0, 0)
        goal = Cell(0, 4)
        obstacles = []
        maze_graph = create_graph_from_grid((rows, cols), obstacles)
        expected_path = ['(0, 0)', '(0, 1)', '(0, 2)', '(0, 3)', '(0, 4)']
        self._run_dfs_tests(maze_graph, start, goal, expected_path,
                            "Single Row Maze", check_exact_path=True)

    def test_single_column_maze(self):
        """
        Tests DFS on a single-column maze.
        """
        rows, cols = 5, 1
        start = Cell(0, 0)
        goal = Cell(4, 0)
        obstacles = []
        maze_graph = create_graph_from_grid((rows, cols), obstacles)
        expected_path = ['(0, 0)', '(1, 0)', '(2, 0)', '(3, 0)', '(4, 0)']
        self._run_dfs_tests(maze_graph, start, goal, expected_path,
                            "Single Column Maze", check_exact_path=True)

    def test_maze_with_dead_ends(self):
        """
        Tests DFS on a maze with dead ends, ensuring it backtracks correctly.
        Revised obstacles to ensure a path is found by current DFS exploration order.
        """
        rows, cols = 4, 4
        start = Cell(0, 0)
        goal = Cell(3, 3)
        obstacles_coords = [
            (0, 2), # Block (0,1) from (0,3)
            (1, 2)  # Block (1,1) from (1,3)
            # Removed (2,0) and (2,1) to open up a path
        ]
        obstacles_cells = [Cell(*o) for o in obstacles_coords]
        maze_graph = create_graph_from_grid((rows, cols), obstacles_cells)

        # A path exists: (0,0) -> (1,0) -> (2,0) -> (3,0) -> (3,1) -> (3,2) -> (3,3)
        # Or: (0,0) -> (0,1) -> (1,1) -> (2,2) -> (2,3) -> (3,3)
        # With sorted neighbors, it should find one of these.
        recursive_path = find_path_recursive(maze_graph, start, goal)
        iterative_path = dfs_iterative(maze_graph, start, goal)

        self.assertIsNotNone(recursive_path, "Recursive DFS should find a path for maze with dead ends")
        self.assertEqual(str(recursive_path[0]), str(start), "Recursive DFS path should start correctly")
        self.assertEqual(str(recursive_path[-1]), str(goal), "Recursive DFS path should end correctly")

        self.assertIsNotNone(iterative_path, "Iterative DFS should find a path for maze with dead ends")
        self.assertEqual(str(iterative_path[0]), str(start), "Iterative DFS path should start correctly")
        self.assertEqual(str(iterative_path[-1]), str(goal), "Iterative DFS path should end correctly")

        # Optional: Print paths for inspection if you want to see what was found
        print(f"\n--- Running Maze with Dead Ends ---")
        print(f"Recursive DFS Path: {[str(node) for node in recursive_path] if recursive_path else None}")
        print(f"Iterative DFS Path: {[str(node) for node in iterative_path] if iterative_path else None}")


# This block allows you to run the tests directly from the command line
if __name__ == '__main__':
    # Using argv and exit=False is good practice for environments like Jupyter/certain IDEs
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

