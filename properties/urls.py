from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    # The list view is now handled by the root URL in config/urls.py
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('my-page/', views.my_page, name='my_page'),
    path('map/', views.map, name='map'),
    path('favorites/', views.favorites, name='favorites'),
    path('news/', views.news, name='news'),
    path('weather/', views.weather, name='weather'),
    path('announcements/', views.announcements, name='announcements'),
    path('announcements/announcement_detail.html/', views.announcement_detail, name='announcement_detail'),
]