def dfs(node, goal, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []
        
    if node == goal:
        path.append(node)
        return True, path.copy()
    
    visited.add(node)
    path.append(node)
    
    for neighbor in node.neighbors:  # Assuming node has a neighbors attribute
        if neighbor not in visited:
            found, result_path = dfs(neighbor, goal, visited, path)
            if found:
                return True, result_path
    
    path.pop()  # Backtrack
    return False, []