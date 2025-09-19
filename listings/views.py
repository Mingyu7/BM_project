from django.shortcuts import render, get_object_or_404, redirect
from listings.models import Property
from weather import services as weather_services
from announcements import services as announcement_services
from announcements.models import Announcement # Import Announcement model
from .forms import PropertyForm
from django.contrib.auth.decorators import login_required

def property_list(request):
    """
    메인 페이지 역할을 겸하는 매물 목록 페이지 뷰입니다.
    최신 매물, 날씨, 뉴스, 공지사항을 함께 제공합니다.
    """
    properties = Property.objects.order_by('-id')[:6]
    weather_list = weather_services.fetch_weather(cities_to_fetch=['서울', '인천', '수원', '천안', '대전'])
    news_list = announcement_services.fetch_news()
    
    # Fetch top 5 announcements
    announcements_list = Announcement.objects.order_by('-created_at')[:5]

    context = {
        'properties': properties,
        'weather_list': weather_list,
        'news_list': news_list,
        'announcements_list': announcements_list,
    }
    return render(request, 'listings/property_main.html', context)


def property_detail(request, pk):
    """
    매물 상세 페이지 뷰입니다.
    """
    property_obj = get_object_or_404(Property, pk=pk)
    context = {
        'property': property_obj,
    }
    return render(request, 'listings/property_detail.html', context)

@login_required
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.author = request.user
            property.save()
            return redirect('listings:property_detail', pk=property.pk)
    else:
        form = PropertyForm()
    return render(request, 'listings/property_form.html', {'form': form})


@login_required
def property_update(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    if property_obj.author != request.user:
        # You can redirect to a 'permission denied' page or just the detail page
        return redirect('listings:property_detail', pk=pk)

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        if form.is_valid():
            form.save()
            return redirect('listings:property_detail', pk=pk)
    else:
        form = PropertyForm(instance=property_obj)
    return render(request, 'listings/property_form.html', {'form': form})


@login_required
def property_delete(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    if property_obj.author != request.user:
        return redirect('listings:property_detail', pk=pk)

    if request.method == 'POST':
        property_obj.delete()
        return redirect('listings:home')
    return render(request, 'listings/property_confirm_delete.html', {'property': property_obj})


def property_index(request):
    region = request.GET.get('region')
    if region:
        properties = Property.objects.filter(region=region).order_by('-id')
    else:
        properties = Property.objects.all().order_by('-id')

    regions = Property.REGION_CHOICES

    context = {
        'properties': properties,
        'regions': regions,
        'selected_region': region,
    }
    return render(request, 'listings/property_list.html', context)