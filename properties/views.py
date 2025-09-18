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

def get_weather_data(cities_to_fetch=None):
    """OpenWeatherMap API에서 현재 날씨 정보를 가져옵니다."""
    api_key = 'f3bc0fab5a87054b1b7f4499c7fcd511'  # settings.py 또는 환경 변수에서 가져오는 것을 권장합니다.
    if not api_key:
        return []

    # 조회할 전체 도시 목록 (영문 이름, 한글 이름, 좌표)
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

    # 조회할 도시 목록 결정
    cities_to_process = all_cities
    if cities_to_fetch:
        cities_to_process = [city for city in all_cities if city['kr'] in cities_to_fetch]

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
                # 지도 페이지를 위해 좌표 정보 추가
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

#뉴스 api
import requests
import json
from datetime import datetime, date, timedelta
from django.conf import settings


def property_list(request):
    properties = Property.objects.order_by('-id')[:6]

    # 더미 데이터 대신 실제 날씨 데이터 가져오기
    weather_list = get_weather_data(cities_to_fetch=['서울', '인천', '수원', '천안', '대전'])

    # (기존 더미 데이터는 여기서 삭제됩니다)
    dummy_news = [
        {'title': '정부, 새로운 부동산 정책 발표', 'date': date(2025, 9, 12)},
        {'title': '서울 아파트값 3주 연속 안정세', 'date': date(2025, 9, 11)},
        {'title': '전세 사기 예방을 위한 새로운 앱 출시', 'date': date(2025, 9, 10)},
        {'title': '가을 이사철, 주목해야 할 지역은?', 'date': date(2025, 9, 9)},
        {'title': '1인 가구를 위한 주거 지원 확대', 'date': date(2025, 9, 8)},
    ]
    dummy_announcements = [
        {'title': '[공지] 추석 연휴 고객센터 운영 안내', 'date': date(2025, 9, 10)},
        {'title': '[업데이트] 새로운 매물 필터 기능 추가', 'date': date(2025, 9, 5)},
        {'title': '[이벤트] 친구 추천하고 포인트 받으세요!', 'date': date(2025, 9, 1)},
        {'title': '[중요] 개인정보 처리방침 개정 안내', 'date': date(2025, 8, 28)},
        {'title': '[안내] 서버 점검 예정 (9/15 02:00~04:00)', 'date': date(2025, 8, 25)},
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

#pip show requests 아무것도 안뜨면
#pip install requests 설치
#뉴스 api연동으로 최근 일주일 기사 9개 가져와 news.html로 넘기기
def news(request, iso_date=None):
    url = "https://newsapi.org/v2/everything"

    today = datetime.today().strftime("%Y-%m-%d")
    week_ago = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")

    params = {
        "q": "부동산",
        "apiKey": "a584b94efeac408e8c34f448fc5fee6d",
        "from": week_ago,
        "to": today
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()  # 전체 dict
        articles = data.get("articles", [])  # 여기서 기사 리스트 가져오기

        # publishedAt 기준 내림차순 정렬
        sorted_news = sorted(
            articles,
            key=lambda x: datetime.strptime(x.get("publishedAt", today+"T00:00:00Z"), "%Y-%m-%dT%H:%M:%SZ"),
            reverse=True
        )

        top_news = sorted_news[:9]

        context = {}
        context = {
            "news_list": [
                {
                    "title": n.get("title", ""),
                    "description": n.get("description", ""),
                    "published_date": datetime.strptime(n.get("publishedAt", today + "T00:00:00Z"), "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d"),
                    "author": n.get("author", ""),
                    "image": n.get("urlToImage", ""),
                    "url": n.get("url", "")
                }
                for n in top_news
            ]
        }
    except Exception as e:
        print("News API Error:", e)
    return render(request, 'properties/news.html', context)



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