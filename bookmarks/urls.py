from django.urls import path
from . import views

app_name = 'bookmarks'

urlpatterns = [
    path('favorites/', views.favorites, name='favorites'),
    path('remove/<int:property_id>/', views.remove_favorite, name='remove_favorite'),
]

