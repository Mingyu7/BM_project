# models.py
from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    # 광역시/도 선택지 정의
    REGION_CHOICES = [
        ("서울특별시", "서울특별시"),
        ("부산광역시", "부산광역시"),
        ("대구광역시", "대구광역시"),
        ("인천광역시", "인천광역시"),
        ("광주광역시", "광주광역시"),
        ("대전광역시", "대전광역시"),
        ("울산광역시", "울산광역시"),
    ]

    # 작성자 필드 추가, 기존 데이터는 null 허용
    author = models.ForeignKey(
        User,
        verbose_name="작성자",
        on_delete=models.CASCADE,
        related_name="properties",
        null=True,   # 기존 데이터에는 비워둘 수 있게
        blank=True
    )

    title = models.CharField("매물이름", max_length=255, db_index=True)
    latitude = models.DecimalField("위도", max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField("경도", max_digits=9, decimal_places=6, null=True, blank=True)
    region = models.CharField("지역", max_length=20, choices=REGION_CHOICES)
    description = models.TextField("설명", blank=True)
    image = models.ImageField("이미지", upload_to="property_images/", null=True, blank=True)
    created_at = models.DateTimeField("생성날짜", auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.region})"

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
        ordering = ["-created_at"]


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
