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

def fetch_weather(cities_to_fetch=None):
    """OpenWeatherMap에서 날씨 가져오기"""
    api_key = 'f3bc0fab5a87054b1b7f4499c7fcd511'
    if not api_key:
        return []

    all_cities = [
        {'en': 'Seoul', 'kr': '서울', 'top': '83%', 'left': '43%'},  #100에 가까울수록 아래로 100에 가까울수록 오른쪽으로 붙어
        {'en': 'Incheon', 'kr': '인천', 'top': '83%', 'left': '40%'}, #ㅇㅋ
        {'en': 'Chuncheon', 'kr': '춘천', 'top': '74%', 'left': '49%'}, #ㅇㅋ
        {'en': 'Gangneung', 'kr': '강릉', 'top': '83%', 'left': '60%'}, #ㅇㅋ
        {'en': 'Suwon', 'kr': '수원', 'top': '90%', 'left': '43%'}, # ㅇㅋ
        {'en': 'Cheongju', 'kr': '청주', 'top': '107%', 'left': '47%'}, #ㅇㅋ
        {'en': 'Cheonan', 'kr': '천안', 'top': '101%', 'left': '44%'}, #ㅇㅋ
        {'en': 'Andong', 'kr': '안동', 'top': '111%', 'left': '59%'}, #ㅇㅋ
        {'en': 'Pohang', 'kr': '포항', 'top': '120%', 'left': '65%'}, #ㅇㅋ
        {'en': 'Daejeon', 'kr': '대전', 'top': '113%', 'left': '45%'}, #ㅇㅋ
        {'en': 'Jeonju', 'kr': '전주', 'top': '123%', 'left': '43%'},
        {'en': 'Daegu', 'kr': '대구', 'top': '123%', 'left': '57%'}, # ㅇㅋ
        {'en': 'Gwangju', 'kr': '광주', 'top': '140%', 'left': '39%'}, #ㅇㅋ
        {'en': 'Mokpo', 'kr': '목포', 'top': '148%', 'left': '36%'},# ㅇㅋ
        {'en': 'Yeosu', 'kr': '여수', 'top': '150%', 'left': '48%'}, #ㅇㅋ
        {'en': 'Jeju', 'kr': '제주', 'top': '177%', 'left': '37%'}, # ㅇㅋ
        {'en': 'Busan', 'kr': '부산', 'top': '141%', 'left': '62%'}, #ㅇㅋ
        {'en': 'Ulsan', 'kr': '울산', 'top': '133%', 'left': '64%'}, # ㅇㅋ
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
