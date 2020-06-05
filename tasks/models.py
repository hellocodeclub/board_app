from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from projects.models import Project,Workspace
from accounts.models import Account
from tasks.choices import status_choices
from django.utils import timezone
from board.constants import *

# Create your models here.

class Task(models.Model):
    assigned_user = models.ForeignKey(Account, on_delete=models.DO_NOTHING,
                                      blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project,on_delete=models.DO_NOTHING)
    estimated_hours = models.DecimalField(default=0.00,max_digits=100, decimal_places=2)
    status = models.CharField(max_length=30)
    workspace = models.ForeignKey(Workspace, on_delete=models.DO_NOTHING)
    priority = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class Cycle(models.Model):
    goal_title = models.CharField(max_length=300)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.DO_NOTHING)
    tasks = models.ManyToManyField(Task)
    def __str__(self):
        return self.goal_title

class CycleHistoryData(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    duration = models.DurationField()
    workspace = models.ForeignKey(Workspace, on_delete=models.DO_NOTHING)
    planned_hours = models.DecimalField(default=0.00,max_digits=100, decimal_places=2)
    done_hours = models.DecimalField(default=0.00,max_digits=100, decimal_places=2)

def get_active_cycle(workspace_id):
    active_cycle = Cycle.objects.filter(workspace=workspace_id,start_date__lte=timezone.now(), end_date__gte=timezone.now()).exclude(goal_title=DEFAULT_CYCLE_TITLE)
    if(active_cycle):
        active_cycle = active_cycle[0]
    else:
        active_cycle= Cycle.objects.filter(workspace=workspace_id, goal_title=DEFAULT_CYCLE_TITLE)[0]
    return active_cycle

def get_default_cycle(workspace_id):
    return Cycle.objects.filter(workspace=workspace_id, goal_title=DEFAULT_CYCLE_TITLE)[0]


def count_open_tasks(workspace_id):
    active_cycle = get_active_cycle(workspace_id)
    if(not active_cycle.tasks):
        return []
    tasks = Task.objects.filter(models.Q(cycle__id=active_cycle.id))
    if(tasks):
        return 10
    else:
        return 0

def get_tasks_on_board(workspace_id):
    active_cycle = get_active_cycle(workspace_id)
    if(not active_cycle.tasks):
        return []
    tasks = Task.objects.filter(models.Q(cycle__id=active_cycle.id))
    return tasks

def get_pending_tasks_outside_board(workspace_id):
    tasks = get_tasks_on_board(workspace_id)
    ids_tasks_on_board = [task.id for task in tasks]
    all_tasks_pending = Task.objects.filter(workspace_id=workspace_id).exclude(status='DONE').exclude(id__in=ids_tasks_on_board)
    return all_tasks_pending.count()



def get_list_tasks_by_status(workspace_id):

    tasks = get_tasks_on_board(workspace_id)
    open_tasks = tasks.filter(status='OPEN').order_by('-updated_at')
    ready_tasks = tasks.filter(status='READY').order_by('-updated_at')
    in_progress_tasks = tasks.filter(status='IN_PROGRESS').order_by('-updated_at')
    test = tasks.filter(status='TEST').order_by('-updated_at')
    done = tasks.filter(status='DONE').order_by('-updated_at')

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

def calculate_completed_hours(workspace_id):
    tasks = get_tasks_on_board(workspace_id)
    completed_tasks = tasks.filter(status='DONE').aggregate(hours=Coalesce(Sum('estimated_hours'),0))
    total_tasks = tasks.aggregate(hours=Coalesce(Sum('estimated_hours'),0))
    board_progress_summary = {
        'completed_tasks': completed_tasks.get('hours'),
        'total_tasks': total_tasks.get('hours'),
        'completed_percentage': calculate_percentage(completed_tasks.get('hours'),total_tasks.get('hours'))
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
        'test_tasks_hours': calculate_percentage(test_hours['hours'],total_tasks_hours['hours']),
        'done_tasks_hours': calculate_percentage(done_hours['hours'],total_tasks_hours['hours'])
    }
    return status
