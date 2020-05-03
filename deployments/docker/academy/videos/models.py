from django.db import models


class VideoTopic(models.Model):
    name    = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    
    class Meta:
        managed     = True
        ordering    = ['name']


class Video(models.Model):
    name        = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    link        = models.CharField(max_length=500)
    duration    = models.CharField(max_length=10)
    topic       = models.ForeignKey(VideoTopic, on_delete=models.CASCADE)

    class Meta:
        managed     = True
        ordering    = ['name']