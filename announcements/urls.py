from django.urls import path
from . import views

app_name = 'announcements'

urlpatterns = [
    path('news/', views.news, name='news'),
    path('announcements/', views.announcements, name='announcements'),
    path('announcements/<int:pk>/', views.announcement_detail, name='announcement_detail'),
    path('announcements/create/', views.announcement_create, name='announcement_create'),
    path('announcements/<int:pk>/delete/', views.announcement_delete, name='announcement_delete'),
]