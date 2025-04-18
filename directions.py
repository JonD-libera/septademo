
import requests

def get_walking_directions(start, end):
    url = f"http://router.project-osrm.org/route/v1/walking/{start[1]},{start[0]};{end[1]},{end[0]}?overview=false&steps=true"
    # Check if the distance between start and end is too far for a reasonable walking distance
    if abs(start[0] - end[0]) > 0.1 or abs(start[1] - end[1]) > 0.1:
        return {"error": "Distance too far for a normal human"}
    resp = requests.get(url)
    return resp.json()
