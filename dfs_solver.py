# dfs_solver.py

# Assuming Cell class is imported from graph_model.py or defined identically here
from graph_model import Cell

def dfs_recursive(graph, current_node, goal_node, visited, path):
    """
    Recursive Depth-First Search (DFS) to find a path.

    :param graph: Adjacency list.
    :param current_node: Current Cell.
    :param goal_node: Target Cell.
    :param visited: Set of visited Cells (for cycle detection).
    :param path: List tracking current path from start to current_node.
    :return: True if path to goal found, False otherwise.
    """
    visited.add(current_node)
    path.append(current_node)

    if current_node == goal_node:
        return True

    for neighbor in graph.get(current_node, []):
        if neighbor not in visited:
            if dfs_recursive(graph, neighbor, goal_node, visited, path):
                return True

    path.pop() # Backtrack
    return False

def find_path_recursive(graph, start_node, goal_node):
    """
    Wrapper for recursive DFS.

    :param graph: Adjacency list.
    :param start_node: Starting Cell.
    :param goal_node: Target Cell.
    :return: List of Cells forming path, or None if no path.
    """
    visited = set()
    path = []
    if dfs_recursive(graph, start_node, goal_node, visited, path):
        return path
    return None

def dfs_iterative(graph, start_node, goal_node):
    """
    Iterative Depth-First Search (DFS) using an explicit stack.

    :param graph: Adjacency list.
    :param start_node: Starting Cell.
    :param goal_node: Target Cell.
    :return: List of Cells forming path, or None if no path.
    """
    stack = [(start_node, [start_node])] # (node, current_path)
    visited = {start_node}

    while stack:
        current_node, path = stack.pop()

        if current_node == goal_node:
            return path

        for neighbor in reversed(graph.get(current_node, [])):
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = path + [neighbor]
                stack.append((neighbor, new_path))
    
    return None
