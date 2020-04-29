from django.contrib import admin
from .models import Task,Cycle, CycleTaskAssociation
# Register your models here.

admin.site.register(Task)
admin.site.register(Cycle)
admin.site.register(CycleTaskAssociation)