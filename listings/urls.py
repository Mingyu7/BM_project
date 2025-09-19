from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('', views.property_list, name='home'),
    path('<int:pk>/', views.property_detail, name='property_detail'),
]
