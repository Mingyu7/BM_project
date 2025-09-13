from django.shortcuts import render, get_object_or_404
from .models import Property

def property_list(request):
    properties = Property.objects.all()
    return render(request, 'properties/property_list.html', {'properties': properties})

def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    return render(request, 'properties/property_detail.html', {'property': property})

# Placeholder views for new pages
def my_page(request):
    return render(request, 'properties/my_page.html')

def favorites(request):
    return render(request, 'properties/favorites.html')

def news(request):
    return render(request, 'properties/news.html')

def weather(request):
    return render(request, 'properties/weather.html')

def announcements(request):
    return render(request, 'properties/announcements.html')
