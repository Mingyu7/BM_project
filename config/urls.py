from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from properties import views as properties_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', properties_views.property_list, name='home'),  # Set home page to property list
    path('accounts/', include('accounts.urls')),
    path('properties/', include('properties.urls', namespace='properties')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)