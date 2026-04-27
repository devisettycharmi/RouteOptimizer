from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union

class Location(BaseModel):
    id: str
    name: str
    lat: float
    lng: float
    type: str = "delivery"

class EdgeWeight(BaseModel):
    distance: float
    time: float
    traffic_multiplier: float = 1.0
    weight: float

class GraphUpdateRequest(BaseModel):
    locations: List[Location]
    edges: Dict[str, Dict[str, Union[EdgeWeight, float]]]

class RouteRequest(BaseModel):
    start: str
    end: str
    intermediate_stops: Optional[List[str]] = []
    algorithm: str = "dijkstra" # dijkstra, floyd_warshall, mst
    
class RouteResponse(BaseModel):
    distance: float
    path: List[str]
    locations: List[Location]
