import os
import requests
import logging
from requests.auth import HTTPBasicAuth
from json import JSONDecodeError
from .errors import EmissionsDataError

# Get an instance of a logger
logger = logging.getLogger(__name__)

WATTTIME_API_TOKEN = os.environ.get("WATTTIME_API_TOKEN")
WATTTIME_API_URL = "https://api.watttime.org/v3"

def get_grid_region(latitude: float, longitude: float):
    """
    Get the grid region for a given location.
    """
    if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
        raise ValueError("Invalid coordinates")

    headers = {
        "Authorization": f"Bearer {WATTTIME_API_TOKEN}",
        "Accept": "application/json",
    }
    params = {"latitude": latitude, "longitude": longitude}
    try:
        response = requests.get(f"{WATTTIME_API_URL}/region-from-loc", headers=headers, params=params)
        logger.info(f"Watttime API response for get_grid_region: {response.text}")

        if response.status_code != 200:
            raise EmissionsDataError(f"WattTime API returned {response.status_code}")

        if not response.text.strip():
            raise EmissionsDataError("Empty response from WattTime API")

        if 'application/json' not in response.headers.get('Content-Type', ''):
            raise EmissionsDataError("Non-JSON response received")

        try:
            return response.json()['region']
        except JSONDecodeError as e:
            raise EmissionsDataError(f"JSON parsing failed: {e}. Response: {response.text[:100]}") from e
        except KeyError:
            raise EmissionsDataError("Could not find 'region' in Watttime API response.")

    except requests.exceptions.RequestException as e:
        raise EmissionsDataError(f"Error getting grid region: {e}") from e


def get_realtime_emissions(grid_region: str):
    """
    Get real-time emissions data for a given grid region.
    """
    headers = {
        "Authorization": f"Bearer {WATTTIME_API_TOKEN}",
        "Accept": "application/json",
    }
    params = {"region": grid_region, "style": "all"}
    try:
        response = requests.get(f"{WATTTIME_API_URL}/signal/index", headers=headers, params=params)
        logger.info(f"Watttime API response for get_realtime_emissions: {response.text}")

        if response.status_code != 200:
            raise EmissionsDataError(f"WattTime API returned {response.status_code}")

        if not response.text.strip():
            raise EmissionsDataError("Empty response from WattTime API")

        if 'application/json' not in response.headers.get('Content-Type', ''):
            raise EmissionsDataError("Non-JSON response received")

        try:
            data = response.json()
            if 'data' not in data or not data['data']:
                raise EmissionsDataError("Could not find 'data' in Watttime API response.")
            if 'percent' not in data['data'][0]:
                raise EmissionsDataError("Could not find 'percent' in Watttime API response.")
            return data['data'][0]
        except JSONDecodeError as e:
            raise EmissionsDataError(f"JSON parsing failed: {e}. Response: {response.text[:100]}") from e

    except requests.exceptions.RequestException as e:
        raise EmissionsDataError(f"Error getting real-time emissions: {e}") from e
