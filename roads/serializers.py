from rest_framework import serializers
from .models import Road

class RoadSerializer(serializers.ModelSerializer):
    # ← 追加：フォームに出さない（API出力のみ）
    name_i18n = serializers.JSONField(read_only=True)
    description_i18n = serializers.JSONField(read_only=True)

    class Meta:
        model = Road
        fields = "__all__"