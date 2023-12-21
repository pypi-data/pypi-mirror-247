"Emoji model"
import uuid
from django.db import models
from django.contrib.auth.models import User


class EmojiManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(deleted_at__isnull=True, image__isnull=False)
        )


class EmojiUpdateManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class Emoji(models.Model):
    EXPORT_FIELDS = [
        "name",
        "uses",
        "created_at",
        "created_by",
        "deleted_at",
        "deleted_by",
    ]

    name = models.CharField(max_length=255, primary_key=True)
    uses = models.IntegerField(default=0)
    image = models.BinaryField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, related_name="created_emojis", on_delete=models.CASCADE
    )
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        User,
        related_name="deleted_emojis",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    objects = EmojiManager()
    updates = EmojiUpdateManager()
    all_objects = models.Manager()
