from django.db import models

class Property(models.Model):
<<<<<<< HEAD
    title = models.CharField(max_length=200)
=======
    PROPERTY_TYPE_CHOICES = [
        ('APARTMENT', '아파트'),
        ('OFFICETEL', '오피스텔'),
        ('ONE_ROOM', '원룸'),
        ('TWO_ROOM', '투룸'),
        ('VILLA', '빌라/주택'),
    ]

    title = models.CharField(max_length=200)
    property_type = models.CharField(
        max_length=10,
        choices=PROPERTY_TYPE_CHOICES,
        default='APARTMENT'
    )
>>>>>>> ba04c90 (up2)
    address = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField()
    photo = models.ImageField(upload_to='property_photos/', blank=True, null=True)

    def __str__(self):
        return self.title