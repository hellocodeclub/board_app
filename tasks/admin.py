from django.contrib import admin
from .models import Task,Cycle
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id','title','project','estimated_hours','status')
    list_display_links = ('id','title')

class CycleAdmin(admin.ModelAdmin):
    list_display = ('id','goal_title','start_date','end_date','workspace')
    list_display_links = ('id','goal_title')

admin.site.register(Task, TaskAdmin)
admin.site.register(Cycle, CycleAdmin)
