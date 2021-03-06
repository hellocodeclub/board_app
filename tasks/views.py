from django.shortcuts import render, redirect
from tasks.models import Task, Cycle, get_tasks_on_board, get_active_cycle, get_default_cycle
from projects.models import Project, Workspace
from tasks.choices import next_state, previous_state
from board.constants import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import TaskForm
from .service import save_or_update_task, remove_task, end_activate_cycle
from notifications.signals import notify
from affilliateproducts.models import AffilliateProduct
from django.contrib.auth.models import User
from .models import CycleHistoryData


# Create your views here.

@login_required(login_url='login')
def task_next_state(request):
    if (request.method == 'POST'):
        task_id = request.POST[TASK_FORM_ID]
        workspace_id = request.session.get(SESSION_WORKSPACE_KEY_NAME)
        task_to_update = Task.objects.filter(id=task_id, workspace=workspace_id)[0]

        if(task_to_update):
            next_status=next_state(task_to_update.status)
            task_to_update.status=next_status
            task_to_update.save()
        return redirect('dashboard')
    else:
        return render(request, 'accounts/dashboard.html')

@login_required(login_url='login')
def task_previous_state(request):
    if(request.method == 'POST'):
        task_id = request.POST[TASK_FORM_ID]
        workspace_id = request.session.get(SESSION_WORKSPACE_KEY_NAME)
        task_to_update = Task.objects.filter(id=task_id, workspace=workspace_id)[0]
        if(task_to_update):
            next_status=previous_state(task_to_update.status)
            task_to_update.status=next_status
            task_to_update.save()

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@login_required(login_url='login')
def task_increase_priority(request):
    if (request.method == 'POST'):
        task_id = request.POST[TASK_FORM_ID]
        workspace_id = request.session.get(SESSION_WORKSPACE_KEY_NAME)
        task_to_update = Task.objects.filter(id=task_id, workspace=workspace_id)[0]

        if(task_to_update):
            current_priority = task_to_update.priority
            task_to_update.priority = current_priority+1
            task_to_update.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@login_required(login_url='login')
def save_task(request):
    if (request.method == 'POST'):
        # read the form
        task_form = TaskForm(request)

        workspace_id = request.session.get(SESSION_WORKSPACE_KEY_NAME)
        save_or_update_task(task_form,workspace_id)

    # redirect to origin site
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@login_required(login_url='login')
def tasks(request):
    workspace_id = request.session.get(SESSION_WORKSPACE_KEY_NAME)
    tasks = Task.objects.filter(workspace=workspace_id).order_by('-updated_at')
    projects = Project.objects.all()
    affiliate_products = AffilliateProduct.objects.all()

    context = {
        'tasks':tasks,
        'projects': projects,
        'recomendations': affiliate_products
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

        default_cycle = get_default_cycle(workspace_id)
        default_cycle.tasks.clear()

        return redirect('dashboard')

    else:
        return redirect('dashboard')

@login_required(login_url='login')
def end_cycle(request):
    workspace_id = request.session.get(SESSION_WORKSPACE_KEY_NAME)
    end_activate_cycle(workspace_id)
    return redirect('dashboard')


@login_required(login_url='login')
def create_notification(request):
    user = None
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
    notify.send(user, recipient=user, verb='test notification')

@login_required(login_url='login')
def reports(request):
    workspace_id = request.session.get(SESSION_WORKSPACE_KEY_NAME)
    cycle_history_entries = CycleHistoryData.objects.filter(workspace=workspace_id)
    context = {
        'cycle_history_entries': cycle_history_entries
    }
    return render(request, 'projects/reports.html',context)












