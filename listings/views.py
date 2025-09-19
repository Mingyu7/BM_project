from django.shortcuts import render, get_object_or_404
from listings.models import Property
from weather import services as weather_services
from announcements import services as announcement_services
from announcements.models import Announcement # Import Announcement model

def property_list(request):
    """
    메인 페이지 역할을 겸하는 매물 목록 페이지 뷰입니다.
    최신 매물, 날씨, 뉴스, 공지사항을 함께 제공합니다.
    """
    properties = Property.objects.order_by('-id')[:6]
    weather_list = weather_services.fetch_weather(cities_to_fetch=['서울', '인천', '수원', '천안', '대전'])
    news_list = announcement_services.fetch_news()

    # 최신 공지사항 5개 가져오기
    announcements_list = Announcement.objects.order_by('-created_at')[:5]

    context = {
        'properties': properties,
        'weather_list': weather_list,
        'news_list': news_list,
        'announcements_list': announcements_list,
    }
    return render(request, 'listings/property_list.html', context)


def property_detail(request, pk):
    """
    매물 상세 페이지 뷰입니다.
    """
    property_obj = get_object_or_404(Property, pk=pk)
    context = {
        'property': property_obj,
    }
    return render(request, 'listings/property_detail.html', context)