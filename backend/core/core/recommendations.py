from .watttime import get_grid_region, get_realtime_emissions
from .errors import EmissionsDataError

def get_ph_recommendations(latitude: float, longitude: float):
    """
    Returns a list of energy-saving recommendations relevant to the Philippines.
    """
    try:
        grid_region = get_grid_region(latitude, longitude)
    except (EmissionsDataError, ValueError) as e:
        return {"error": f"EMISSIONS_DATA: {e}"}

    if not grid_region:
        grid_region = "PH" # Default to Philippines grid region

    try:
        emissions = get_realtime_emissions(grid_region)
    except EmissionsDataError as e:
        return {"error": f"EMISSIONS_DATA: {e}"}


    if not emissions:
        return {"error": "EMISSIONS_DATA: Could not get real-time emissions data."}

    if "error" in emissions:
        return {"error": f"EMISSIONS_DATA: {emissions['error']}"}

    if "percent" not in emissions:
        return {"error": "EMISSIONS_DATA: Could not find 'percent' in emissions data."}

    if emissions["percent"] < 50:
        return [
            "The grid is currently running on clean energy. It's a good time to run your appliances.",
            "Take advantage of the clean energy and charge your devices.",
        ]
    else:
        return [
            "The grid is currently running on dirty energy. Try to reduce your energy consumption.",
            "Postpone running your appliances until the grid is cleaner.",
        ]
