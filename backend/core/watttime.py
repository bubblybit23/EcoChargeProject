import os
import requests

WATTTIME_API_TOKEN = os.environ.get("WATTTIME_API_TOKEN")
WATTTIME_API_URL = "https://api.watttime.org/v2/"

def get_realtime_emissions(latitude: float, longitude: float):
    """
    Get real-time emissions data for a given location.
    """
    headers = {"Authorization": f"Bearer {WATTTIME_API_TOKEN}"}
    params = {"latitude": latitude, "longitude": longitude}
    response = requests.get(f"{WATTTIME_API_URL}emissions", headers=headers, params=params)
    response.raise_for_status()
    return response.json()
