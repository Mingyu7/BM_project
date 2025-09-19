from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('', views.property_list, name='home'),
    path('index/', views.property_index, name='property_index'),
    path('create/', views.property_create, name='property_create'),
    path('<int:pk>/', views.property_detail, name='property_detail'),
]
