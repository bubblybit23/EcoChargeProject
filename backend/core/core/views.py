from django.http import JsonResponse
from core.recommendations import get_ph_recommendations

def recommendations(request):
    """
    Returns a list of energy-saving recommendations.
    """
    return JsonResponse(get_ph_recommendations(), safe=False)
