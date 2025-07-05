from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:  # noqa: D106
        model = User
        fields = "__all__"
