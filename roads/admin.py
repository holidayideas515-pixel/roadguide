from django.contrib import admin
from .models import Road

@admin.register(Road)
class RoadAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "length_km", "time_min", "updated_at")
    search_fields = ("name", "slug")