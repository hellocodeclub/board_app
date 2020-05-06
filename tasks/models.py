from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from datetime import datetime
from projects.models import Project,Workspace
from accounts.models import Account
from tasks.choices import status_choices

# Create your models here.

class Task(models.Model):
    assigned_user = models.ForeignKey(Account, on_delete=models.DO_NOTHING, blank=True)
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
        'status': status_choices['open'],
        'tasks': open_tasks
    })
    list.append({
        'status': status_choices['ready'],
        'tasks': ready_tasks
    })
    list.append({
        'status': status_choices['in_progress'],
        'tasks': in_progress_tasks
    })
    list.append({
        'status': status_choices['test'],
        'tasks': test
    })
    list.append({
        'status': status_choices['done'],
        'tasks': done
    })
    return list

def calculate_percentage(partial,total):
    if total == 0:
        return 0
    return int((partial/total)*100)

def calculate_completed_hours():
    completed_tasks = Task.objects.filter(status='DONE').aggregate(hours=Coalesce(Sum('estimated_hours'),0))
    total_tasks = Task.objects.aggregate(hours=Coalesce(Sum('estimated_hours'),0))
    board_progress_summary = {
        'completed_tasks': completed_tasks['hours'],
        'total_tasks': total_tasks['hours'],
        'completed_percentage': calculate_percentage(completed_tasks['hours'],total_tasks['hours'])
    }
    return board_progress_summary

def caclulate_status_percentages(project):
    total_tasks_hours = Task.objects.filter(project=project).aggregate(hours=Coalesce(Sum('estimated_hours'),0))
    open_tasks_hours = Task.objects.filter(project=project).filter(status='OPEN').aggregate(hours=Coalesce(Sum('estimated_hours'),0))
    ready_tasks_hours = Task.objects.filter(project=project).filter(status='READY').aggregate(hours=Coalesce(Sum('estimated_hours'),0))
    in_progress_tasks_hours = Task.objects.filter(project=project).filter(status='IN_PROGRESS').aggregate(hours=Coalesce(Sum('estimated_hours'),0))
    test_hours = Task.objects.filter(project=project).filter(status='TEST').aggregate(hours=Coalesce(Sum('estimated_hours'),0))
    done_hours = Task.objects.filter(project=project).filter(status='DONE').aggregate(hours=Coalesce(Sum('estimated_hours'),0))
    status = {
        'open_tasks_hours': calculate_percentage(open_tasks_hours['hours'],total_tasks_hours['hours']),
        'ready_tasks_hours': calculate_percentage(ready_tasks_hours['hours'],total_tasks_hours['hours']),
        'in_progress_tasks_hours': calculate_percentage(in_progress_tasks_hours['hours'],total_tasks_hours['hours']),
        'test_hours': calculate_percentage(test_hours['hours'],total_tasks_hours['hours']),
        'done_hours': calculate_percentage(done_hours['hours'],total_tasks_hours['hours'])
    }
    return status
