from rest_framework import serializers

from .models import Message, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:  # noqa: D106
        model = User
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:  # noqa: D106
        model = Message
        fields = ("id", "content", "sender_id", "recipient_id", "created_at")
