from django.contrib import admin
from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'region', 'price', 'created_at')
    list_filter = ('region',)
    search_fields = ('title', 'description')