from rest_framework import serializers
from .models import FlipBook

class FlipBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlipBook
        fields = ["id", "title", "pdf_file", "flipbook_url", "created_at"]
