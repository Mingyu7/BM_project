from django.shortcuts import render, get_object_or_404
from .models import Property
import datetime

def property_list(request):
    properties = Property.objects.order_by('-id')[:6] # Show latest 6 properties

    # Dummy data for new sections
    dummy_news = [
        {'title': '정부, 새로운 부동산 정책 발표', 'date': datetime.date(2025, 9, 12)},
        {'title': '서울 아파트값 3주 연속 안정세', 'date': datetime.date(2025, 9, 11)},
        {'title': '전세 사기 예방을 위한 새로운 앱 출시', 'date': datetime.date(2025, 9, 10)},
        {'title': '가을 이사철, 주목해야 할 지역은?', 'date': datetime.date(2025, 9, 9)},
        {'title': '1인 가구를 위한 주거 지원 확대', 'date': datetime.date(2025, 9, 8)},
    ]

    dummy_weather = [
        {'location': '서울', 'temp': '22°C', 'condition': '맑음'},
        {'location': '부산', 'temp': '24°C', 'condition': '구름 조금'},
        {'location': '대구', 'temp': '25°C', 'condition': '맑음'},
        {'location': '인천', 'temp': '21°C', 'condition': '흐림'},
        {'location': '광주', 'temp': '23°C', 'condition': '비'},
    ]

    dummy_announcements = [
        {'title': '[공지] 추석 연휴 고객센터 운영 안내', 'date': datetime.date(2025, 9, 10)},
        {'title': '[업데이트] 새로운 매물 필터 기능 추가', 'date': datetime.date(2025, 9, 5)},
        {'title': '[이벤트] 친구 추천하고 포인트 받으세요!', 'date': datetime.date(2025, 9, 1)},
        {'title': '[중요] 개인정보 처리방침 개정 안내', 'date': datetime.date(2025, 8, 28)},
        {'title': '[안내] 서버 점검 예정 (9/15 02:00~04:00)', 'date': datetime.date(2025, 8, 25)},
    ]

    context = {
        'properties': properties,
        'news_list': dummy_news,
        'weather_list': dummy_weather,
        'announcements_list': dummy_announcements,
    }
    return render(request, 'properties/property_list.html', context)

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

def announcement_detail(request):
    return render(request, 'properties/announcement_detail.html')

def map(request):
    return render(request, 'properties/map.html')
