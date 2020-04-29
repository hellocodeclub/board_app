from django.db import models
from datetime import datetime
from projects.models import Project,Workspace
from users.models import User

# Create your models here.

class Task(models.Model):
    assigned_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project,on_delete=models.DO_NOTHING)
    estimated_hours = models.IntegerField(blank=True)
    status = models.CharField(max_length=30)
    workspace = models.ForeignKey(Workspace, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.title

class Cycle(models.Model):
    goal_title = models.CharField(max_length=300)
    start_date = models.DateTimeField(default=datetime.now)
    end_date = models.DateTimeField(blank=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.goal_title

class CycleTaskAssociation(models.Model):
    cycle = models.ForeignKey(Cycle, on_delete=models.DO_NOTHING)
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)


def get_dictionary_tasks_by_status():

    open_tasks = Task.objects.filter(status='OPEN')
    ready_tasks = Task.objects.filter(status='READY')
    in_progress_tasks = Task.objects.filter(status='IN_PROGRESS')
    test = Task.objects.filter(status='TEST')
    done = Task.objects.filter(status='DONE')
    list = []
    list.append({
        'status': 'open',
        'tasks': open_tasks
    })
    list.append({
        'status': 'ready',
        'tasks': ready_tasks
    })
    list.append({
        'status': 'in_progress',
        'tasks': in_progress_tasks
    })
    list.append({
        'status': 'test',
        'tasks': test
    })
    list.append({
        'status': 'done',
        'tasks': done
    })
    return list
