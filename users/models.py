from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=150)
    avatar = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)

