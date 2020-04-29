from django.db import models
from users.models import User

# Create your models here.
class Workspace(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

class Project(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.DO_NOTHING)
    color = models.CharField(max_length=10)
