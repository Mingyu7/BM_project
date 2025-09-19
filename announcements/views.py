from django.shortcuts import render, get_object_or_404
from . import services
from .models import Announcement # Import Announcement model

def news(request):
    context = {
        "news_list": services.fetch_news()
    }
    return render(request, 'announcements/news.html', context)

def announcements(request):
    announcements_list = Announcement.objects.order_by('-created_at')
    context = {
        'announcements_list': announcements_list
    }
    return render(request, 'announcements/announcements.html', context)

def announcement_detail(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    context = {
        'announcement': announcement
    }
    return render(request, 'announcements/announcement_detail.html', context)