from django.shortcuts import render, get_object_or_404
from .models import Property
import requests
import datetime

# --- OpenWeatherMap API 아이콘 매핑 ---
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


def get_weather_data(cities_to_fetch=None):
    api_key = 'f3bc0fab5a87054b1b7f4499c7fcd511'
    if not api_key:
        return []

    all_cities = [
        {'en': 'Seoul', 'kr': '서울', 'top': '18%', 'left': '33%'},
        {'en': 'Incheon', 'kr': '인천', 'top': '22%', 'left': '22%'},
        {'en': 'Chuncheon', 'kr': '춘천', 'top': '12%', 'left': '45%'},
        {'en': 'Gangneung', 'kr': '강릉', 'top': '15%', 'left': '68%'},
        {'en': 'Suwon', 'kr': '수원', 'top': '28%', 'left': '32%'},
        {'en': 'Cheongju', 'kr': '청주', 'top': '38%', 'left': '45%'},
        {'en': 'Cheonan', 'kr': '천안', 'top': '33%', 'left': '38%'},
        {'en': 'Andong', 'kr': '안동', 'top': '40%', 'left': '65%'},
        {'en': 'Pohang', 'kr': '포항', 'top': '50%', 'left': '80%'},
        {'en': 'Daejeon', 'kr': '대전', 'top': '48%', 'left': '40%'},
        {'en': 'Jeonju', 'kr': '전주', 'top': '60%', 'left': '35%'},
        {'en': 'Daegu', 'kr': '대구', 'top': '60%', 'left': '65%'},
        {'en': 'Gwangju', 'kr': '광주', 'top': '73%', 'left': '30%'},
        {'en': 'Mokpo', 'kr': '목포', 'top': '80%', 'left': '20%'},
        {'en': 'Yeosu', 'kr': '여수', 'top': '83%', 'left': '48%'},
        {'en': 'Jeju', 'kr': '제주', 'top': '92%', 'left': '25%'},
        {'en': 'Busan', 'kr': '부산', 'top': '70%', 'left': '75%'},
        {'en': 'Ulsan', 'kr': '울산', 'top': '62%', 'left': '82%'},
    ]

    cities_to_process = all_cities if not cities_to_fetch else [
        city for city in all_cities if city['kr'] in cities_to_fetch
    ]

    weather_list = []

    for city in cities_to_process:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city['en']}&appid={api_key}&units=metric&lang=kr"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            main_weather = data.get('main', {})
            weather_info = data.get('weather', [{}])[0]

            temp = main_weather.get('temp')
            description = weather_info.get('description')
            icon_code = weather_info.get('icon')
            icon_class = WEATHER_ICON_MAP.get(icon_code, "fas fa-question-circle")

            if temp is not None and description:
                weather_data = {
                    'location': city['kr'],
                    'temp': f"{temp:.0f}°",
                    'condition': description,
                    'icon': icon_class,
                }
                if not cities_to_fetch:
                    weather_data['top'] = city['top']
                    weather_data['left'] = city['left']
                weather_list.append(weather_data)
            else:
                raise requests.exceptions.RequestException(f"Incomplete data for {city['kr']}")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather for {city['kr']}: {e}")
            error_data = {
                'location': city['kr'],
                'temp': 'N/A',
                'condition': '정보 없음',
                'icon': 'fas fa-exclamation-circle',
            }
            if not cities_to_fetch:
                error_data['top'] = city['top']
                error_data['left'] = city['left']
            weather_list.append(error_data)

    return weather_list


def property_list(request):
    properties = Property.objects.order_by('-id')[:6]
    weather_list = get_weather_data(cities_to_fetch=['서울', '인천', '수원', '천안', '대전'])

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
        'weather_list': weather_list,
        'announcements_list': dummy_announcements,
    }
    return render(request, 'properties/property_list.html', context)


def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    return render(request, 'properties/property_detail.html', {'property': property})


def my_page(request):
    return render(request, 'properties/my_page.html')


def favorites(request):
    return render(request, 'properties/favorites.html')


def news(request):
    return render(request, 'properties/news.html')


def weather(request):
    context = {'weather_list': get_weather_data()}
    return render(request, 'properties/weather.html', context)


def announcements(request):
    return render(request, 'properties/announcements.html')


def announcement_detail(request):
    return render(request, 'properties/announcement_detail.html')


def map(request):
    return render(request, 'properties/map.html')
