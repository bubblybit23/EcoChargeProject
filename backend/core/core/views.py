from django.http import JsonResponse
from .recommendations import get_ph_recommendations

def recommendations(request):
    """
    Returns a list of energy-saving recommendations.
    """
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')

    if not latitude or not longitude:
        return JsonResponse({'error': 'latitude and longitude are required'}, status=400)

    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        return JsonResponse({'error': 'latitude and longitude must be numbers'}, status=400)

    return JsonResponse(get_ph_recommendations(latitude, longitude), safe=False)
