from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Sound(models.Model):
    name = models.CharField(max_length=140)
    text = models.CharField(max_length=280, null=True)
    sound_file = models.FileField(upload_to='sounds/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_file = models.FileField(upload_to='sound_images/', null=True)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'text': self.text,
            'image_file': '/media/' + self.image_file.url,
            'sound_file': '/media/' + self.sound_file.url,
        }

# class SoundBoard(models.Model):
#     name = models.CharField(max_length=140)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
