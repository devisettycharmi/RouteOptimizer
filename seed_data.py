import requests

# Mock locations for Indian Cities
locations = [
    {"id": "MUM", "name": "Mumbai Warehouse", "lat": 19.0760, "lng": 72.8777, "type": "warehouse"},
    {"id": "DEL", "name": "Delhi Hub", "lat": 28.7041, "lng": 77.1025, "type": "delivery"},
    {"id": "BLR", "name": "Bangalore Tech Park", "lat": 12.9716, "lng": 77.5946, "type": "delivery"},
    {"id": "HYD", "name": "Hyderabad Terminal", "lat": 17.3850, "lng": 78.4867, "type": "delivery"},
    {"id": "MAA", "name": "Chennai Port", "lat": 13.0827, "lng": 80.2707, "type": "delivery"}
]

# Graph with approximate distances
edges = {
    "MUM": {
        "DEL": {"distance": 1400.0, "time": 1400, "traffic_multiplier": 1.1, "weight": 1540.0},
        "BLR": {"distance": 980.0, "time": 980, "traffic_multiplier": 1.0, "weight": 980.0},
        "HYD": {"distance": 710.0, "time": 710, "traffic_multiplier": 1.2, "weight": 852.0}
    },
    "DEL": {
        "MUM": {"distance": 1400.0, "time": 1400, "traffic_multiplier": 1.1, "weight": 1540.0},
        "HYD": {"distance": 1500.0, "time": 1500, "traffic_multiplier": 1.0, "weight": 1500.0},
    },
    "BLR": {
        "MUM": {"distance": 980.0, "time": 980, "traffic_multiplier": 1.0, "weight": 980.0},
        "HYD": {"distance": 570.0, "time": 570, "traffic_multiplier": 1.5, "weight": 855.0},
        "MAA": {"distance": 350.0, "time": 350, "traffic_multiplier": 1.0, "weight": 350.0}
    },
    "HYD": {
        "MUM": {"distance": 710.0, "time": 710, "traffic_multiplier": 1.2, "weight": 852.0},
        "DEL": {"distance": 1500.0, "time": 1500, "traffic_multiplier": 1.0, "weight": 1500.0},
        "BLR": {"distance": 570.0, "time": 570, "traffic_multiplier": 1.5, "weight": 855.0},
        "MAA": {"distance": 630.0, "time": 630, "traffic_multiplier": 1.0, "weight": 630.0}
    },
    "MAA": {
        "BLR": {"distance": 350.0, "time": 350, "traffic_multiplier": 1.0, "weight": 350.0},
        "HYD": {"distance": 630.0, "time": 630, "traffic_multiplier": 1.0, "weight": 630.0}
    }
}

try:
    response = requests.post(
        "http://127.0.0.1:8000/update_graph",
        json={"locations": locations, "edges": edges}
    )
    print("Seed Data Response:", response.json())
except Exception as e:
    print("Error connecting to API. Make sure FastAPI server is running.", e)
