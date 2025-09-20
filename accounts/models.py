from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='이름')
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True, verbose_name='프로필 사진')
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name='전화번호')
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name='주소')

    def __str__(self):
        return self.user.username


