from django.db import models

class Property(models.Model):
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField()
    photo = models.ImageField(upload_to='property_photos/', blank=True, null=True)

    def __str__(self):
        return self.title