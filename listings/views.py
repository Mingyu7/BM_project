from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
import requests
from listings.models import Property
from weather import services as weather_services
from announcements import services as announcement_services
from announcements.models import Announcement # Import Announcement model
from .forms import PropertyForm
from django.contrib.auth.decorators import login_required
from bookmarks.models import Favorite # Import Favorite model for bookmarking

def property_list(request):
    """
    메인 페이지 역할을 겸하는 매물 목록 페이지 뷰입니다.
    최신 매물, 날씨, 뉴스, 공지사항을 함께 제공합니다.
    """
    properties = Property.objects.order_by('-id')[:6]
    weather_list = weather_services.fetch_weather(cities_to_fetch=['서울', '인천', '수원', '천안', '대전'])
    news_list = announcement_services.fetch_news()
    
    # Fetch top 5 announcements
    announcements_list = Announcement.objects.order_by('-created_at')[:5]

    bookmarked_properties = []
    if request.user.is_authenticated:
        bookmarked_properties = Favorite.objects.filter(user=request.user).values_list('property__id', flat=True)

    context = {
        'properties': properties,
        'weather_list': weather_list,
        'news_list': news_list,
        'announcements_list': announcements_list,
        'bookmarked_properties': list(bookmarked_properties), # 템플릿에 전달
    }
    return render(request, 'listings/property_main.html', context)


def property_detail(request, pk):
    """
    매물 상세 페이지 뷰입니다.
    """
    property_obj = get_object_or_404(Property, pk=pk)
    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = Favorite.objects.filter(user=request.user, property=property_obj).exists()

    context = {
        'property': property_obj,
        'is_bookmarked': is_bookmarked, # 템플릿에 전달
    }
    return render(request, 'listings/property_detail.html', context)

@login_required
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_instance = form.save(commit=False)
            property_instance.author = request.user

            # Geocoding logic
            address = form.cleaned_data.get('address')
            if address:
                print(f"--- Geocoding Start (Debug) ---")
                print(f"Address to geocode: {address}")
                
                try:
                    url = "https://dapi.kakao.com/v2/local/search/address.json"
                    headers = {"Authorization": f"KakaoAK {settings.KAKAO_REST_API_KEY}"}
                    params = {"query": address}
                    
                    print(f"Request URL: {url}")
                    print(f"Request Headers (partial key): {{'Authorization': 'KakaoAK ...{settings.KAKAO_REST_API_KEY[-4:]}'}}")
                    
                    response = requests.get(url, headers=headers, params=params)
                    response.raise_for_status() # Raise an exception for bad status codes
                    data = response.json()
                    
                    print(f"API Response: {data}")

                    if data.get("documents"):
                        coords = data["documents"][0]
                        property_instance.latitude = coords["y"]
                        property_instance.longitude = coords["x"]
                        print(f"Coordinates found: Lat={coords['y']}, Lng={coords['x']}")
                    else:
                        print("No documents found in API response.")

                except requests.exceptions.RequestException as e:
                    print(f"Error calling Kakao API: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                
                print("--- Geocoding End (Debug) ---")

            property_instance.save()
            return redirect('listings:property_detail', pk=property_instance.pk)
    else:
        form = PropertyForm()
    return render(request, 'listings/property_form.html', {'form': form})


@login_required
def property_update(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    if property_obj.author != request.user:
        return redirect('listings:property_detail', pk=pk)

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        if form.is_valid():
            property_instance = form.save(commit=False)

            # Geocoding logic
            address = form.cleaned_data.get('address')
            if address:
                url = "https://dapi.kakao.com/v2/local/search/address.json"
                headers = {"Authorization": f"KakaoAK {settings.KAKAO_REST_API_KEY}"}
                params = {"query": address}
                response = requests.get(url, headers=headers, params=params).json()

                if response.get("documents"):
                    coords = response["documents"][0]
                    property_instance.latitude = coords["y"]
                    property_instance.longitude = coords["x"]
                else: # If geocoding fails, maybe clear the coordinates?
                    property_instance.latitude = None
                    property_instance.longitude = None

            property_instance.save()
            return redirect('listings:property_detail', pk=pk)
    else:
        form = PropertyForm(instance=property_obj)
    return render(request, 'listings/property_form.html', {'form': form})


@login_required
def property_delete(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    if property_obj.author != request.user:
        return redirect('listings:property_detail', pk=pk)

    if request.method == 'POST':
        property_obj.delete()
        return redirect('listings:home')
    return render(request, 'listings/property_confirm_delete.html', {'property': property_obj})


from django.contrib.auth.decorators import login_required
from bookmarks.models import Favorite # Import Favorite model


def property_index(request):
    region = request.GET.get('region')
    if region:
        properties = Property.objects.filter(region=region).order_by('-id')
    else:
        properties = Property.objects.all().order_by('-id')

    regions = Property.REGION_CHOICES
    
    bookmarked_properties = []
    if request.user.is_authenticated:
        bookmarked_properties = Favorite.objects.filter(user=request.user).values_list('property__id', flat=True)

    context = {
        'properties': properties,
        'regions': regions,
        'selected_region': region,
        'bookmarked_properties': list(bookmarked_properties), # 템플릿에 전달
    }

    return render(request, 'listings/property_list.html', context)

#''로 접속했을때 'listings'로 리다이렉트
def myhome(request):
    return redirect('/listings/')
    return render(request, 'listings/property_list.html', context)
