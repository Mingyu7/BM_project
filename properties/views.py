from django.shortcuts import render, get_object_or_404
from .models import Property
from . import services # 서비스 레이어 import

def property_list(request):
    """
    메인 페이지 역할을 겸하는 매물 목록 페이지 뷰입니다.
    최신 매물, 날씨, 뉴스, 공지사항을 함께 제공합니다.
    """
    properties = Property.objects.order_by('-id')[:6]
    weather_list = services.fetch_weather(cities_to_fetch=['서울', '인천', '수원', '천안', '대전'])
    news_list = services.fetch_news()

    # 실제 DB 연동이 필요하지만, 임시 데이터 사용
    dummy_announcements = [
        {'title': '[공지] 추석 연휴 고객센터 운영 안내', 'date': '2025-09-10', 'pk': 1},
        {'title': '[업데이트] 새로운 매물 필터 기능 추가', 'date': '2025-09-05', 'pk': 2},
    ]

    context = {
        'properties': properties,
        'weather_list': weather_list,
        'news_list': news_list,
        'announcements_list': dummy_announcements,
    }
    return render(request, 'properties/property_list.html', context)


def property_detail(request, pk):
    """
    매물 상세 페이지 뷰입니다.
    """
    property_obj = get_object_or_404(Property, pk=pk)
    context = {
        'property': property_obj,
    }
    return render(request, 'properties/property_detail.html', context)

# ----------------- 기타 뷰는 유지 -----------------
def my_page(request):
    return render(request, 'properties/my_page.html')

def favorites(request):
    return render(request, 'properties/favorites.html')

def news(request):
    context = {
        "news_list": services.fetch_news()
    }
    return render(request, 'properties/news.html', context)

def weather(request):
    weather_list = services.fetch_weather(cities_to_fetch=None)
    context = {'weather_list': weather_list}
    return render(request, 'properties/weather.html', context)

def announcements(request):
    return render(request, 'properties/announcements.html')

def announcement_detail(request, pk):
    # 실제 구현 시 DB에서 공지사항을 가져와야 함
    return render(request, 'properties/announcement_detail.html')

def map(request):
    return render(request, 'properties/map.html')