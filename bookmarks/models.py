from django.db import models
from django.contrib.auth.models import User
from listings.models import Property

class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="유저",
        on_delete=models.CASCADE,
        related_name="favorites",
    )
    property = models.ForeignKey(
        Property,
        verbose_name="매물",
        on_delete=models.CASCADE,
        related_name="favorited_by",
    )
    created_at = models.DateTimeField("생성일", auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.property.title}"

    class Meta:
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"
        unique_together = ("user", "property")