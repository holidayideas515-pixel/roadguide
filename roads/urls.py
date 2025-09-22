from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoadViewSet

router = DefaultRouter()
router.register(r"roads", RoadViewSet, basename="roads")

urlpatterns = [
    path("", include(router.urls)),
]