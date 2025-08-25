# graph_model.py

class Cell:
    """Represents a single cell (vertex) in the grid-based maze."""
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __hash__(self):
        """Enables Cell objects to be used in sets and as dictionary keys."""
        return hash((self.row, self.col))

    def __eq__(self, other):
        """Defines equality for Cell objects based on coordinates."""
        if not isinstance(other, Cell):
            return NotImplemented
        return self.row == other.row and self.col == other.col

    def __repr__(self):
        """Provides a string representation for debugging."""
        return f"({self.row}, {self.col})"

def create_graph_from_grid(grid_dims, obstacles):
    """
    Creates an adjacency list from a grid, representing cells as vertices and
    valid moves as edges. Handles obstacles and grid boundaries.

    :param grid_dims: Tuple (rows, cols) of grid dimensions.
    :param obstacles: List of Cell objects representing wall locations.
    :return: Adjacency list (dict of Cell -> list of Cell).
    """
    rows, cols = grid_dims
    graph = {}
    obstacle_cells = set(obstacles) # For efficient lookup

    # Define 4-directional movements (Up, Down, Left, Right)
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]

    for r in range(rows):
        for c in range(cols):
            current_cell = Cell(r, c)

            # Obstacles have no outgoing edges
            if current_cell in obstacle_cells:
                graph[current_cell] = []
                continue

            neighbors_list = []
            for i in range(4): # Check all 4 directions
                neighbor_row, neighbor_col = r + dr[i], c + dc[i]
                neighbor_cell = Cell(neighbor_row, neighbor_col)

                # Check bounds and if neighbor is an obstacle
                is_within_bounds = (0 <= neighbor_row < rows) and (0 <= neighbor_col < cols)
                is_not_obstacle = neighbor_cell not in obstacle_cells

                if is_within_bounds and is_not_obstacle:
                    neighbors_list.append(neighbor_cell)
            
            # Sort neighbors for predictable DFS traversal order
            graph[current_cell] = sorted(neighbors_list, key=lambda cell: (cell.row, cell.col))
    
    return graph

