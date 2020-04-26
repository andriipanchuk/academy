from django.db import models

# Create your models here.


class Videos(models.Model):
    name        = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    embed_code  = models.CharField(max_length=500)
    
