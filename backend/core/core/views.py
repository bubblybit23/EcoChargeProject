import json
from django.http import JsonResponse
from .recommendations import get_ph_recommendations

def recommendations(request):
    """
    Returns a list of energy-saving recommendations.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            latitude = data['lat']
            longitude = data['lng']
            return JsonResponse(get_ph_recommendations(latitude, longitude), safe=False)
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid location data'}, status=400)
    elif request.method == 'GET':
        # Use a default location for GET requests
        latitude = 14.5995
        longitude = 120.9842
        return JsonResponse(get_ph_recommendations(latitude, longitude), safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
