from django.shortcuts import render, get_object_or_404, redirect
from . import services
from .models import Announcement
from django.contrib.auth.decorators import login_required
from .forms import AnnouncementForm

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

@login_required
def announcement_create(request):
    if not request.user.is_superuser:
        return redirect('announcements:announcements')
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            announcement.save()
            return redirect('announcements:announcement_detail', pk=announcement.pk)
    else:
        form = AnnouncementForm()
    context = {'form': form}
    return render(request, 'announcements/announcement_form.html', context)

@login_required
def announcement_delete(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.user.is_superuser:
        announcement.delete()
    return redirect('announcements:announcements')