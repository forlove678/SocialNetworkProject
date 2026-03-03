from collections import deque

def get_connections(adj_list, start_node, degree=1):
    visited = {start_node}
    queue = deque([(start_node, 0)])
    results = []

    while queue:
        curr, d = queue.popleft()
        if 0 < d <= degree:
            results.append(curr)
        if d < degree:
            for neighbor in adj_list.get_neighbors(curr):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, d + 1))
    return results