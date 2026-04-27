def run_floyd_warshall(graph: dict):
    """
    Floyd-Warshall Algorithm to find shortest distances between all pairs of vertices.
    Time Complexity: O(V^3)
    
    graph: dict of dicts e.g., {'A': {'B': 5.0, 'C': 2.0}, 'B': {'A': 5.0}, 'C': {'A': 2.0}}
    """
    nodes = list(graph.keys())
    dist = {n1: {n2: float('inf') for n2 in nodes} for n1 in nodes}
    next_node = {n1: {n2: None for n2 in nodes} for n1 in nodes}
    
    # Initialize distances
    for n in nodes:
        dist[n][n] = 0
        
    for u in nodes:
        for v, weight_info in graph[u].items():
            weight = weight_info if isinstance(weight_info, (int, float)) else weight_info.get('weight', 1)
            dist[u][v] = weight
            next_node[u][v] = v
            
    # Floyd-Warshall Algorithm
    for k in nodes:
        for i in nodes:
            for j in nodes:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]
                    
    return {"distances": dist, "next_node": next_node}

def reconstruct_path_floyd_warshall(u: str, v: str, next_node: dict):
    """
    Reconstructs shortest path from u to v using next_node matrix.
    """
    if next_node[u][v] is None:
        return []
        
    path = [u]
    while u != v:
        u = next_node[u][v]
        path.append(u)
    return path
