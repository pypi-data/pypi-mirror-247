"""Emoticons URLs."""

from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from .viewsets import EmojiViewSet
from .routers import EmojiRouter

app_name = "emojis"

router = EmojiRouter(trailing_slash=False)
router.register("emoticon", EmojiViewSet, basename="emoticons")

urlpatterns = [
    path("", include(router.urls)),
]
