from django.db import models

# Create your models here.
class Sound(models.Model):
    name = models.CharField(max_length=140)
