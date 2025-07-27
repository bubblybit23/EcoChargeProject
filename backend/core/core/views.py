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
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
