from django.shortcuts import render
from . import services

def weather(request):
    weather_list = services.fetch_weather(cities_to_fetch=None)
    context = {'weather_list': weather_list}
    return render(request, 'weather/weather.html', context)