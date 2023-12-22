"""Emoticons serializer."""

from django.utils.translation import gettext_lazy as _
from .models import Emoji
from rest_framework import serializers


class EmojiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emoji
        fields = "__all__"


class EmojiListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emoji
        fields = ["name"]


class EmojiDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Emoji
        fields = []


class EmojiCreateSerializer(serializers.ModelSerializer):
    image = serializers.FileField(label=_("File"), required=False)

    class Meta:
        model = Emoji
        fields = ["image"]
