from django.shortcuts import render, get_object_or_404
from .models import Property
import datetime
import requests

# --- OpenWeatherMap API 아이콘 매핑 ---
# OpenWeatherMap에서 제공하는 날씨 아이콘 코드를 Font Awesome 아이콘 클래스로 변환합니다.
WEATHER_ICON_MAP = {
    "01d": "fas fa-sun", "01n": "fas fa-moon",
    "02d": "fas fa-cloud-sun", "02n": "fas fa-cloud-moon",
    "03d": "fas fa-cloud", "03n": "fas fa-cloud",
    "04d": "fas fa-cloud-meatball", "04n": "fas fa-cloud-meatball",
    "09d": "fas fa-cloud-showers-heavy", "09n": "fas fa-cloud-showers-heavy",
    "10d": "fas fa-cloud-sun-rain", "10n": "fas fa-cloud-moon-rain",
    "11d": "fas fa-poo-storm", "11n": "fas fa-poo-storm",
    "13d": "far fa-snowflake", "13n": "far fa-snowflake",
    "50d": "fas fa-smog", "50n": "fas fa-smog",
}

def get_weather_data():
    """OpenWeatherMap One Call API 3.0에서 날씨 정보를 가져옵니다."""
    api_key = 'f3bc0fab5a87054b1b7f4499c7fcd511' # API 키를 직접 입력합니다.
    if not api_key:
        return []

    # 도시별 위도, 경도 정보
    cities = {
        '서울': {'lat': 37.5665, 'lon': 126.9780},
        '부산': {'lat': 35.1796, 'lon': 129.0756},
        '대구': {'lat': 35.8714, 'lon': 128.6014},
        '인천': {'lat': 37.4563, 'lon': 126.7052},
        '광주': {'lat': 35.1595, 'lon': 126.8526},
    }
    weather_list = []

    for city_name, coords in cities.items():
        lat = coords['lat']
        lon = coords['lon']
        # One Call API 3.0 URL
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,daily,alerts&appid={api_key}&units=metric&lang=kr"
        
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            current_weather = data.get('current', {})
            if not current_weather:
                raise requests.exceptions.RequestException("API 응답에 'current' 키가 없습니다.")

            weather_info = current_weather.get('weather', [{}])[0]
            icon_code = weather_info.get('icon')
            icon_class = WEATHER_ICON_MAP.get(icon_code, "fas fa-question-circle")

            weather_list.append({
                'location': city_name,
                'temp': f"{current_weather.get('temp', 'N/A'):.1f}°C",
                'condition': weather_info.get('description', '정보 없음'),
                'icon': icon_class,
            })
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather for {city_name}: {e}")
            weather_list.append({
                'location': city_name,
                'temp': 'N/A',
                'condition': '정보 없음',
                'icon': 'fas fa-exclamation-circle',
            })
    return weather_list

def property_list(request):
    properties = Property.objects.order_by('-id')[:6]

    # 더미 데이터 대신 실제 날씨 데이터 가져오기
    weather_list = get_weather_data()

    # (기존 더미 데이터는 여기서 삭제됩니다)
    dummy_news = [
        {'title': '정부, 새로운 부동산 정책 발표', 'date': datetime.date(2025, 9, 12)},
        {'title': '서울 아파트값 3주 연속 안정세', 'date': datetime.date(2025, 9, 11)},
        {'title': '전세 사기 예방을 위한 새로운 앱 출시', 'date': datetime.date(2025, 9, 10)},
        {'title': '가을 이사철, 주목해야 할 지역은?', 'date': datetime.date(2025, 9, 9)},
        {'title': '1인 가구를 위한 주거 지원 확대', 'date': datetime.date(2025, 9, 8)},
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
        'weather_list': weather_list, # 실제 날씨 데이터로 교체
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

def news(request):
    return render(request, 'properties/news.html')

def weather(request):
    # 이 뷰도 실제 날씨 데이터를 보여주도록 수정할 수 있습니다.
    context = {'weather_list': get_weather_data()}
    return render(request, 'properties/weather.html', context)

def announcements(request):
    return render(request, 'properties/announcements.html')

def announcement_detail(request):
    return render(request, 'properties/announcement_detail.html')

def map(request):
    return render(request, 'properties/map.html')
