from core.watttime import get_grid_region, get_realtime_emissions

def get_ph_recommendations(latitude: float, longitude: float):
    """
    Returns a list of energy-saving recommendations relevant to the Philippines.
    """
    grid_region = get_grid_region(latitude, longitude)
    if not grid_region:
        return ["Could not determine grid region."]

    emissions = get_realtime_emissions(grid_region)
    if not emissions:
        return ["Could not get real-time emissions data."]

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
