# dfs_solver.py

# Assuming Cell class is imported from graph_model.py or defined identically here
from graph_model import Cell

def dfs_recursive(graph, current_node, goal_node, visited, path, history, depth=0):
    """
    Recursive Depth-First Search (DFS) to find a path and record history.

    :param graph: Adjacency list.
    :param current_node: Current Cell.
    :param goal_node: Target Cell.
    :param visited: Set of visited Cells (for cycle detection).
    :param path: List tracking current path from start to current_node.
    :param history: List to record the sequence of visited nodes.
    :param depth: Current recursion depth.
    :return: Tuple of (found, max_depth).
    """
    visited.add(current_node)
    path.append(current_node)
    history.append(current_node)
    max_depth = depth

    if current_node == goal_node:
        return True, max_depth

    for neighbor in graph.get(current_node, []):
        if neighbor not in visited:
            found, new_depth = dfs_recursive(graph, neighbor, goal_node, visited, path, history, depth + 1)
            max_depth = max(max_depth, new_depth)
            if found:
                return True, max_depth

    path.pop() # Backtrack
    return False, max_depth

def find_path_recursive(graph, start_node, goal_node):
    """
    Wrapper for recursive DFS.

    :param graph: Adjacency list.
    :param start_node: Starting Cell.
    :param goal_node: Target Cell.
    :return: Tuple of (path, history, max_depth). Path is a list of Cells, or None.
    """
    visited = set()
    path = []
    history = []
    found, max_depth = dfs_recursive(graph, start_node, goal_node, visited, path, history)
    if found:
        return path, history, max_depth
    return None, history, max_depth

def dfs_iterative(graph, start_node, goal_node):
    """
    Iterative Depth-First Search (DFS) using an explicit stack.

    :param graph: Adjacency list.
    :param start_node: Starting Cell.
    :param goal_node: Target Cell.
    :return: Tuple of (path, history). Path is a list of Cells, or None. History is a list of visited nodes.
    """
    stack = [(start_node, [start_node])] # (node, current_path)
    visited = {start_node}
    history = []

    while stack:
        current_node, path = stack.pop()
        history.append(current_node)

        if current_node == goal_node:
            return path, history

        for neighbor in reversed(graph.get(current_node, [])):
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = path + [neighbor]
                stack.append((neighbor, new_path))
    
    return None, history
