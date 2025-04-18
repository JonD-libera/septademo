
from fastapi import APIRouter, Request, Query
from rate_limiter import check_rate_limit
from auth import check_auth
from redis_cache import get_cached_result, cache_result
from kmz_loader import load_stations_from_kmz
from directions import get_walking_directions
from config import KMZ_FILE_PATH
from geopy.distance import distance

router = APIRouter()

stations = load_stations_from_kmz(KMZ_FILE_PATH)

@router.get("/nearest_station")
async def nearest_station(request: Request, lat: float = Query(...), lon: float = Query(...)):
    check_auth(request)
    check_rate_limit(request)

    key = f"station:{lat}:{lon}"
    cached = get_cached_result(key)
    if cached:
        return cached

    user_loc = (lat, lon)
    nearest = min(stations, key=lambda s: distance(user_loc, (s["lat"], s["lon"])).km)
    directions = get_walking_directions(user_loc, (nearest["lat"], nearest["lon"]))

    result = {"station": nearest, "directions": directions}
    cache_result(key, result)
    return result
