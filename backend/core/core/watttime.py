import os
import requests
import logging
from requests.auth import HTTPBasicAuth

# Get an instance of a logger
logger = logging.getLogger(__name__)

WATTTIME_API_TOKEN = os.environ.get("WATTTIME_API_TOKEN")
WATTTIME_API_URL = "https://api.watttime.org/v2"


def get_grid_region(latitude: float, longitude: float):
    """
    Get the grid region for a given location.
    """
    headers = {"Authorization": f"Bearer {WATTTIME_API_TOKEN}"}
    params = {"latitude": latitude, "longitude": longitude}
    try:
        response = requests.get(f"{WATTTIME_API_URL}/region-from-loc", headers=headers, params=params)
        logger.info(f"Watttime API response for get_grid_region: {response.text}")
        response.raise_for_status()
        return response.json()["region"]
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting grid region: {e}")
        return None

def get_realtime_emissions(grid_region: str):
    """
    Get real-time emissions data for a given grid region.
    """
    headers = {"Authorization": f"Bearer {WATTTIME_API_TOKEN}"}
    params = {"region": grid_region}
    try:
        response = requests.get(f"{WATTTIME_API_URL}/index", headers=headers, params=params)
        logger.info(f"Watttime API response for get_realtime_emissions: {response.text}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting real-time emissions: {e}")
        return None
