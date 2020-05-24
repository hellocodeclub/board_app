from django.shortcuts import render, redirect
from tasks.models import Task, Cycle, get_tasks_on_board, get_active_cycle
from projects.models import Project, Workspace
from tasks.choices import next_state
from board.constants import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import TaskForm
from .service import save_or_update_task, remove_task
from notifications.signals import notify
from django.contrib.auth.models import User


# Create your views here.

@login_required(login_url='login')
def task_next_state(request):
    if (request.method == 'POST'):
        task_id = request.POST[TASK_FORM_ID]
        workspace_id = request.session.get(SESSION_WORKSPACE_KEY_NAME)
        task_to_update = Task.objects.filter(id=task_id, workspace=workspace_id)

        if(task_to_update):
            next_status=next_state(task_to_update.values('status')[0]['status'])
            task_to_update.update(status=next_status)
        return redirect('dashboard')
    else:
        return render(request, 'accounts/dashboard.html')

@login_required(login_url='login')
def task_increase_priority(request):
    if (request.method == 'POST'):
        task_id = request.POST[TASK_FORM_ID]
        workspace_id = request.session.get(SESSION_WORKSPACE_KEY_NAME)
        task_to_update = Task.objects.filter(id=task_id, workspace=workspace_id)

        if(task_to_update):
            current_priority=task_to_update.values('priority')[0]['priority']
            task_to_update.update(priority=current_priority+1)
        return redirect('dashboard')
    else:
        return redirect('dashboard')

@login_required(login_url='login')
def save_task(request):
    if (request.method == 'POST'):
        # read the form
        task_form = TaskForm(request)

        workspace_id = request.session.get(SESSION_WORKSPACE_KEY_NAME)
        save_or_update_task(task_form,workspace_id)

        return redirect('dashboard')

    else:
        return redirect('dashboard')

@login_required(login_url='login')
def tasks(request):
    workspace_id = request.session.get(SESSION_WORKSPACE_KEY_NAME)
    tasks = Task.objects.filter(workspace=workspace_id).order_by('-priority')
    projects = Project.objects.all()

    context = {
        'tasks':tasks,
        'projects': projects
    }
    return render(request, 'tasks/tasks.html', context)

@login_required(login_url='login')
def delete_task(request):
    if(request.method == 'POST'):
        task_id= request.POST.get('task-id')
        workspace_id = request.session.get(SESSION_WORKSPACE_KEY_NAME)
        remove_task(taskId=task_id, workspaceId=workspace_id)
        return redirect('dashboard')

    else:
        return redirect('dashboard')
@login_required(login_url='login')
def start_cycle(request):
    if (request.method == 'POST'):
        workspace_id = request.session.get(SESSION_WORKSPACE_KEY_NAME)
        goal_title = request.POST.get(START_CYCLE_TITLE)
        duration_in_days = int(request.POST.get(DURATION_CYCLE))
        end_date = timezone.now()+ timezone.timedelta(duration_in_days)
        tasks = get_tasks_on_board(workspace_id)
        workspace = Workspace.objects.filter(id= workspace_id)[0]
        cycle = Cycle(goal_title=goal_title, start_date=timezone.now(), end_date=end_date
                      ,workspace=workspace)
        cycle.save()
        for task in tasks:
            cycle.tasks.add(task)

        return redirect('dashboard')

    else:
        return redirect('dashboard')

@login_required(login_url='login')
def create_notification(request):
    user = None
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
    notify.send(user, recipient=user, verb='test notification')
    return redirect('dashboard')











