import heapq

def run_mst_prim(graph: dict, start_node: str = None):
    """
    Prim's Algorithm to find the Minimum Spanning Tree (MST) of a connected, 
    undirected graph with weighted edges.
    
    graph: dict of dicts e.g., {'A': {'B': 5.0, 'C': 2.0}, 'B': {'A': 5.0}, 'C': {'A': 2.0}}
    """
    if not graph:
        return {"mst": [], "total_cost": 0}
        
    if start_node is None:
        start_node = list(graph.keys())[0]
        
    visited = set([start_node])
    edges = []
    
    # Initialize edges from start_node
    for neighbor, weight_info in graph[start_node].items():
        weight = weight_info if isinstance(weight_info, (int, float)) else weight_info.get('weight', 1)
        heapq.heappush(edges, (weight, start_node, neighbor))
        
    mst = []
    total_cost = 0
    
    while edges and len(visited) < len(graph):
        weight, u, v = heapq.heappop(edges)
        
        if v not in visited:
            visited.add(v)
            mst.append({"source": u, "target": v, "weight": weight})
            total_cost += weight
            
            for neighbor, n_weight_info in graph[v].items():
                if neighbor not in visited:
                    n_weight = n_weight_info if isinstance(n_weight_info, (int, float)) else n_weight_info.get('weight', 1)
                    heapq.heappush(edges, (n_weight, v, neighbor))
                    
    return {"mst": mst, "total_cost": total_cost}
