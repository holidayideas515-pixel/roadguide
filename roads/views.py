from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q

from rest_framework import viewsets, filters as drf_filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter

from .models import Road
from .serializers import RoadSerializer


# JSONField（配列）用フィルタ
class RoadFilter(FilterSet):
    prefectures = CharFilter(method="filter_prefectures")
    tags = CharFilter(method="filter_tags")
    seasonality = CharFilter(method="filter_seasonality")
    slug = CharFilter(field_name="slug", lookup_expr="exact")
    difficulty = CharFilter(field_name="difficulty", lookup_expr="exact")

    class Meta:
        model = Road
        fields = ["prefectures", "tags", "seasonality", "slug", "difficulty"]

    def _any_contains(self, queryset, field_name: str, value: str):
        if not value:
            return queryset
        parts = [v.strip() for v in value.split(",") if v.strip()]
        if not parts:
            return queryset
        q = Q()
        for v in parts:
            q |= Q(**{f"{field_name}__contains": [v]})
        return queryset.filter(q)

    def filter_prefectures(self, queryset, name, value):
        return self._any_contains(queryset, "prefectures", value)

    def filter_tags(self, queryset, name, value):
        return self._any_contains(queryset, "tags", value)

    def filter_seasonality(self, queryset, name, value):
        return self._any_contains(queryset, "seasonality", value)


class RoadViewSet(viewsets.ModelViewSet):
    queryset = Road.objects.all().order_by("-updated_at")
    serializer_class = RoadSerializer
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_class = RoadFilter
    search_fields = ["name", "description"]
    ordering_fields = ["updated_at", "length_km", "time_min", "name"]
    lookup_field = "slug"  # /api/roads/<slug>/


# 地図ページ（/map/）
def map_page(request):
    return render(request, "roads/map.html")


# ヘルスチェック（/healthz/）
def healthz(request):
    return JsonResponse({"status": "ok"})