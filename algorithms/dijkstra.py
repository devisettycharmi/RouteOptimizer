import heapq

def run_dijkstra(graph: dict, start: str, end: str = None):
    """
    Dijkstra's Algorithm to find the shortest path from start node to all other nodes.
    If 'end' is provided, it can return early or return the specific path to 'end'.
    
    graph: dict of dicts e.g., {'A': {'B': 5.0, 'C': 2.0}, 'B': {'A': 5.0}, 'C': {'A': 2.0}}
    """
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    
    priority_queue = [(0, start)]
    previous_nodes = {node: None for node in graph}
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if end and current_node == end:
            break
            
        if current_distance > distances[current_node]:
            continue
            
        for neighbor, weight_info in graph[current_node].items():
            # weight_info could be a numeric weight or a dict with multiple weights (distance, time)
            weight = weight_info if isinstance(weight_info, (int, float)) else weight_info.get('weight', 1)
            
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
                
    # Reconstruct path if end is provided
    if end:
        path = []
        current = end
        while current:
            path.append(current)
            current = previous_nodes[current]
        path.reverse()
        if path[0] == start:
            return {"distance": distances[end], "path": path}
        else:
            return {"distance": float('inf'), "path": []}
            
    return {"distances": distances, "previous_nodes": previous_nodes}

