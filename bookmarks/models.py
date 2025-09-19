from django.db import models
from django.contrib.auth.models import User  # 기본 User 모델 사용
from listings.models import Property        # Property 모델

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')  # 같은 유저가 같은 매물 중복 즐겨찾기 불가
        ordering = ['-created_at']              # 최신 즐겨찾기 순 정렬

    @classmethod
    def get_user_favorites(cls, user):
        """특정 유저의 즐겨찾기 리스트 반환"""
        return cls.objects.filter(user=user).select_related('property')


    def __str__(self):
        return f"{self.user.username} - {self.property.title}"
