from django.shortcuts import render, get_object_or_404
from .models import Property
from datetime import datetime, date, timedelta
# API
import requests
from . import services  # 서비스 레이어 import



def property_list(request):
    properties = Property.objects.order_by('-id')[:6]
    weather_list = services.fetch_weather(cities_to_fetch=['서울','인천','수원','천안','대전'])
    news_list = services.fetch_news()

    dummy_announcements = [
        {'title': '[공지] 추석 연휴 고객센터 운영 안내', 'date': '2025-09-10'},
        {'title': '[업데이트] 새로운 매물 필터 기능 추가', 'date': '2025-09-05'},
        # ...
    ]

    context = {
        'properties': properties,
        'weather_list': weather_list,
        'news_list': news_list,
        'announcements_list': dummy_announcements,
    }
    return render(request, 'properties/property_list.html', context)


def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    return render(request, 'properties/property_detail.html', {'property': property})


# ... (이하 다른 뷰들은 그대로 유지) ...
def my_page(request):
    return render(request, 'properties/my_page.html')


def favorites(request):
    return render(request, 'properties/favorites.html')


# ----------------- 뉴스 뷰 -----------------
def news(request):
    """
    뉴스 페이지 뷰
    """
    context = {
        "news_list": services.fetch_news()  # 서비스 레이어에서 뉴스 가져오기
    }
    return render(request, 'properties/news.html', context)


def weather(request):
    """
    날씨 페이지 뷰 - 모든 도시 보여주기
    """
    weather_list = services.fetch_weather(cities_to_fetch=None)  # 모든 도시
    context = {'weather_list': weather_list}
    return render(request, 'properties/weather.html', context)



def announcements(request):
    return render(request, 'properties/announcements.html')


def announcement_detail(request):
    return render(request, 'properties/announcement_detail.html')


def map(request):
    return render(request, 'properties/map.html')