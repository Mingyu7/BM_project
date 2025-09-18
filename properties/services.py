from datetime import datetime, timedelta
import requests

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

# ----------------- 날씨 관련 -----------------
def fetch_weather(cities_to_fetch=None):
    """OpenWeatherMap에서 날씨 가져오기"""
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

    cities = all_cities if not cities_to_fetch else [c for c in all_cities if c['kr'] in cities_to_fetch]
    weather_list = []

    for city in cities:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city['en']}&appid={api_key}&units=metric&lang=kr"
        try:
            res = requests.get(url, timeout=5)
            res.raise_for_status()
            data = res.json()
            temp = data.get('main', {}).get('temp')
            weather_info = data.get('weather', [{}])[0]
            description = weather_info.get('description')
            icon_code = weather_info.get('icon')
            icon_class = WEATHER_ICON_MAP.get(icon_code, "fas fa-question-circle")

            weather_list.append({
                'location': city['kr'],
                'temp': f"{temp:.0f}°" if temp is not None else "N/A",
                'condition': description or "정보 없음",
                'icon': icon_class,
                'top': city.get('top'),
                'left': city.get('left'),
            })
        except Exception as e:
            weather_list.append({
                'location': city['kr'],
                'temp': 'N/A',
                'condition': '정보 없음',
                'icon': 'fas fa-exclamation-circle',
                'top': city.get('top'),
                'left': city.get('left'),
            })
    return weather_list

# ----------------- 뉴스 관련 -----------------
def fetch_news(query="부동산", days=7, top_n=9):
    """News API에서 최근 뉴스 가져오기"""
    url = "https://newsapi.org/v2/everything"
    api_key = "a584b94efeac408e8c34f448fc5fee6d"

    today = datetime.today()
    week_ago = today - timedelta(days=days)

    params = {"q": query, "apiKey": api_key, "from": week_ago.strftime("%Y-%m-%d"), "to": today.strftime("%Y-%m-%d")}
    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        articles = res.json().get("articles", [])
        sorted_news = sorted(
            articles,
            key=lambda x: datetime.strptime(x.get("publishedAt", today.isoformat()), "%Y-%m-%dT%H:%M:%SZ"),
            reverse=True
        )
        return [{
            "title": n.get("title", ""),
            "description": n.get("description", ""),
            "published_date": datetime.strptime(n.get("publishedAt", today.isoformat()), "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d"),
            "author": n.get("author", ""),
            "image": n.get("urlToImage", ""),
            "url": n.get("url", "")
        } for n in sorted_news[:top_n]]
    except Exception as e:
        print("News API Error:", e)
        return []
