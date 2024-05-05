from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Image(models.Model):
    user = models.ForeignKey(User, related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField()

    def __str__(self):
        return self.image_url