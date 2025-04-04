from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FlipBook, Subscription

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class FlipBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlipBook
        fields = ["id", "user", "title", "pdf_file", "flipbook_url", "created_at"]
        read_only_fields = ["flipbook_url", "user"]  # User & flipbook_url should not be required in the request

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
