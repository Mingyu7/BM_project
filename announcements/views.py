from django.shortcuts import render
from . import services

def news(request):
    context = {
        "news_list": services.fetch_news()
    }
    return render(request, 'announcements/news.html', context)

def announcements(request):
    return render(request, 'announcements/announcements.html')

def announcement_detail(request, pk):
    # 실제 구현 시 DB에서 공지사항을 가져와야 함
    return render(request, 'announcements/announcement_detail.html')