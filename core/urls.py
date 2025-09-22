from django.contrib import admin
from django.urls import path, include
from roads.views import map_page     # ← 追加

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("roads.urls")),
    path("map/", map_page),           # ← 追加
    path("healthz/", healthz),
]