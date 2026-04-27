import os
import sys
# Add parent directory to path to import algorithms
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.models.schemas import RouteRequest, RouteResponse, Location, GraphUpdateRequest
from algorithms import run_dijkstra, run_floyd_warshall, reconstruct_path_floyd_warshall, run_mst_prim

app = FastAPI(title="Route Optimizer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory graph storage for simplicity, can be moved to MongoDB later
# Structure: { 'NodeA': { 'NodeB': 5.0, 'NodeC': 2.0 } }
graph_data = {}
locations_data = {}

@app.get("/")
def read_root():
    return {"message": "Welcome to Route Optimizer API"}

@app.get("/locations")
def get_locations():
    return {"locations": list(locations_data.values()), "graph": graph_data}

@app.post("/update_graph")
def update_graph(request: GraphUpdateRequest):
    global graph_data, locations_data
    graph_data = request.edges
    for loc in request.locations:
        locations_data[loc.id] = loc
    return {"message": "Graph updated successfully."}

@app.post("/calculate_route")
def calculate_route(request: RouteRequest):
    if request.start not in locations_data or (request.end and request.end not in locations_data):
        raise HTTPException(status_code=400, detail="Invalid start or end location ID.")
        
    if request.algorithm == "dijkstra":
        # Note: Doesn't handle TSP natively yet, just point to point
        result = run_dijkstra(graph_data, request.start, request.end)
        
        # Resolve locations
        path_locations = [locations_data.get(node) for node in result.get("path", [])]
        
        return {
            "algorithm": "dijkstra",
            "distance": result.get("distance", -1),
            "path": result.get("path", []),
            "locations": path_locations
        }
        
    elif request.algorithm == "floyd_warshall":
        result = run_floyd_warshall(graph_data)
        dist_matrix = result["distances"]
        next_matrix = result["next_node"]
        
        # If end is specified, reconstruct
        if request.end:
            path = reconstruct_path_floyd_warshall(request.start, request.end, next_matrix)
            dist = dist_matrix[request.start][request.end]
            path_locations = [locations_data.get(node) for node in path]
            return {
                "algorithm": "floyd_warshall",
                "distance": dist,
                "path": path,
                "locations": path_locations
            }
        else:
            return {"algorithm": "floyd_warshall", "result": "All-pairs calculated. Specify end for path."}
            
    elif request.algorithm == "mst":
        result = run_mst_prim(graph_data, request.start)
        return {
            "algorithm": "mst",
            "total_cost": result.get("total_cost", 0),
            "edges": result.get("mst", [])
        }
    
    raise HTTPException(status_code=400, detail="Unknown algorithm")
