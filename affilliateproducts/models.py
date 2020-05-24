from django.db import models

# Create your models here.

class AffilliateProduct(models.Model):
    title = models.CharField(max_length=300)
    image_url = models.TextField()
    redirect_url = models.TextField()
    priority = models.IntegerField(default=0)
    clicked_count = models.IntegerField(default=0)
    def __str__(self):
        return self.title
