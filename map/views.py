from django.shortcuts import render
from django.conf import settings

def map(request):
    return render(request, 'map/map.html', {'KAKAO_API_KEY': settings.KAKAO_API_KEY})