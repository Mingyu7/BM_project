from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from listings import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.myhome),
    path('listings/', include('listings.urls')),
    path('announcements/', include('announcements.urls')),
    path('bookmarks/', include('bookmarks.urls')),
    path('map/', include('map.urls')),
    path('weather/', include('weather.urls')),
    path('accounts/', include('accounts.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)