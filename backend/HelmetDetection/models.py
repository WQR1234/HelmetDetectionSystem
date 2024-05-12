from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Image(models.Model):
    user = models.ForeignKey(User, related_name='images', on_delete=models.CASCADE)
    image_name = models.CharField(max_length=30)
    upload_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.image_name
    

class Video(models.Model):
    user = models.ForeignKey(User, related_name='videos', on_delete=models.CASCADE)
    video_name = models.CharField(max_length=30)
    upload_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.video_name