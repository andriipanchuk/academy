from django.db import models

# Create your models here.


class Video(models.Model):
    name        = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    link        = models.CharField(max_length=500)
    duration    = models.CharField(max_length=10)
