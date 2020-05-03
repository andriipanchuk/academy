from django.db import models


class Video(models.Model):
    name        = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    link        = models.CharField(max_length=500)
    duration    = models.CharField(max_length=10)

    class Meta:
        managed     = True
        ordering    = ['name']


class VideoTopic(models.Model):
    name    = models.CharField(max_length=30)
    video   = models.ForeignKey(Video, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        managed     = True
        ordering    = ['name']
