from datetime import datetime, timedelta
import requests

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
