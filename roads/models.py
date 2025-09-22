import uuid
from django.db import models

class Road(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, db_index=True)        # URLに使う短い名前
    name = models.CharField(max_length=200)                    # 道の表示名
    prefectures = models.JSONField(default=list)               # 例: ["tokyo","kanagawa"]
    tags = models.JSONField(default=list)                      # 例: ["winding","coastal"]
    length_km = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    time_min = models.IntegerField(null=True, blank=True)      # 目安時間（分）
    difficulty = models.IntegerField(default=2)                # 1〜5
    seasonality = models.JSONField(default=list)               # 例: ["spring","autumn"]
    description = models.TextField(blank=True, default="")
    gmaps_url = models.URLField(blank=True, default="")

    # 位置情報はまずは簡単に：GeoJSONをそのまま保存（あとでPostGISに移行しやすい）
    geom_geojson = models.JSONField(null=True, blank=True)     # LineString など

    # 多言語の下準備（後で使う）
    name_i18n = models.JSONField(default=dict, blank=True)
    description_i18n = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name