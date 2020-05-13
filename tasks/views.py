from django.shortcuts import render, redirect
from tasks.models import Task
from projects.models import Project, Workspace
from tasks.choices import next_state
from board.constants import *
from accounts.models import Account
from django.contrib.auth.decorators import login_required

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
        taskId = request.POST[TASK_FORM_ID]
        titleName = request.POST[TASK_FORM_NAME]
        projectId = request.POST[TASK_FORM_PROJECT]
        estimatedHours = request.POST[TASK_FORM_ESTIMATED_HOURS] if request.POST[TASK_FORM_ESTIMATED_HOURS] else 1
        assignedPerson = request.POST[TASK_FORM_ASSIGNED_PERSON]
        status =request.POST[TASK_FORM_STATUS] if request.POST[TASK_FORM_STATUS] else 'OPEN'
        description = request.POST[TASK_FORM_DESCRIPTION]
        project = Project.objects.filter(id=projectId)[0]
        account = Account.objects.filter(username='marta@gmail.com')[0]
        if(not project):
            project = Project.objects.filter(title='Default')[0]
        if(taskId):

            task = Task.objects.filter(id=taskId)[0]
            task.title=titleName
            task.description= description
            task.estimated_hours= estimatedHours
            task.assigned_user = account
            task.status=status
            task.project=project
            task.save()
        else:
            workspace_id = request.session.get(SESSION_WORKSPACE_KEY_NAME)
            workspace = Workspace.objects.filter(id= workspace_id)[0]
            task = Task(title=titleName,description= description,
                        estimated_hours= estimatedHours,status=status, project=project,assigned_user=account, workspace=workspace)
            task.save()

        return redirect('dashboard')

    else:
        return redirect('dashboard')

@login_required(login_url='login')
def tasks(request):
    workspace_id = request.session.get(SESSION_WORKSPACE_KEY_NAME)
    tasks = Task.objects.filter(workspace=workspace_id).order_by('-priority')

    context = {
        'tasks':tasks
    }
    return render(request, 'tasks/tasks.html', context)








