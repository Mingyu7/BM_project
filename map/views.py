from django.shortcuts import render
from .services import get_kakao_maps_api_key

def map(request):
    api_key = get_kakao_maps_api_key()
    return render(request, 'map/map.html', {'api_key': api_key})