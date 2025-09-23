from django.db import models
from django.contrib.auth.models import User
import os

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

    # 작성자 필드
    author = models.ForeignKey(
        User,
        verbose_name="작성자",
        on_delete=models.CASCADE,
        related_name="properties",
        null=True,
        blank=True
    )

    title = models.CharField("매물이름", max_length=255, db_index=True)
    address = models.CharField("주소", max_length=255, blank=True, null=True)
    latitude = models.DecimalField("위도", max_digits=22, decimal_places=16, null=True, blank=True)
    longitude = models.DecimalField("경도", max_digits=22, decimal_places=16, null=True, blank=True)
    region = models.CharField("지역", max_length=20, choices=REGION_CHOICES)
    description = models.TextField("설명", blank=True)
    image = models.ImageField("이미지", upload_to="property_images/", null=True, blank=True)
    price = models.BigIntegerField("가격", null=True, blank=True)  # 💰 가격 필드 추가
    created_at = models.DateTimeField("생성날짜", auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.region}) - {self.price if self.price else '가격 미정'}원"

    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
        ordering = ["-created_at"]