from django.shortcuts import render
from .services import get_kakao_maps_api_key
from listings.models import Property
import json

def map(request):
    api_key = get_kakao_maps_api_key()
    properties = Property.objects.filter(latitude__isnull=False, longitude__isnull=False)
    property_list = []
    for prop in properties:
        property_list.append({
            'pk': prop.pk,
            'title': prop.title,
            'latitude': float(prop.latitude),
            'longitude': float(prop.longitude),
            'price': prop.price
        })

    context = {
        'api_key': api_key,
        'properties_json': json.dumps(property_list)
    }
    return render(request, 'map/map.html', context)