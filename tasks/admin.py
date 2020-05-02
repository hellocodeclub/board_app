from django.contrib import admin
from .models import Task,Cycle, CycleTaskAssociation
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id','title','project','estimated_hours','status')
    list_display_links = ('id','title')

admin.site.register(Task, TaskAdmin)
admin.site.register(Cycle)
admin.site.register(CycleTaskAssociation)