from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    # The list view is now handled by the root URL in config/urls.py
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('my-page/', views.my_page, name='my_page'),
    path('favorites/', views.favorites, name='favorites'),
    path('news/', views.news, name='news'),
    path('weather/', views.weather, name='weather'),
    path('announcements/', views.announcements, name='announcements'),
]