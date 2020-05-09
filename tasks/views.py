from django.shortcuts import render, redirect
from tasks.models import Task
from accounts.models import Account
from projects.models import Project, Workspace
from tasks.choices import next_state
from board.constants import SESSION_WORKSPACE_KEY_NAME

# Create your views here.

def task_next_state(request):
    if (request.method == 'POST'):
        task_id = request.POST['task-id']
        workspace_id = request.session.get(SESSION_WORKSPACE_KEY_NAME)
        task_to_update = Task.objects.filter(id=task_id, workspace=workspace_id)

        if(task_to_update):
            next_status=next_state(task_to_update.values('status')[0]['status'])
            task_to_update.update(status=next_status)
        return redirect('dashboard')
    else:
        return render(request, 'accounts/dashboard.html')
def task_increase_priority(request):
    if (request.method == 'POST'):
        task_id = request.POST['task-id']
        workspace_id = request.session.get(SESSION_WORKSPACE_KEY_NAME)
        task_to_update = Task.objects.filter(id=task_id, workspace=workspace_id)

        if(task_to_update):
            current_priority=task_to_update.values('priority')[0]['priority']
            task_to_update.update(priority=current_priority+1)
        return redirect('dashboard')
    else:
        return redirect('dashboard')


def save_task(request):
    if (request.method == 'POST'):
        taskId = request.POST['task-id']
        titleName = request.POST['title-name']
        projectId = request.POST['project']
        estimatedHours = request.POST['estimated-hours'] if request.POST['estimated-hours'] else 1
        assignedPerson = request.POST['assigned-person']
        status =request.POST['status-task'] if request.POST['status-task'] else 'OPEN'
        description = request.POST['description-text']
        project = Project.objects.filter(id=projectId)[0]
        if(not project):
            project = Project.objects.filter(title='Default')[0]
        if(taskId):

            task = Task.objects.filter(id=taskId)[0]
            task.title=titleName
            task.description= description
            task.estimated_hours= estimatedHours
            task.status=status
            task.project=project
            task.save()
        else:
            account = Account.objects.filter(username='marta@gmail.com')[0]
            workspace = Workspace.objects.filter(id=1)[0]
            task = Task(title=titleName,description= description,
                        estimated_hours= estimatedHours,status=status, project=project,assigned_user=account, workspace=workspace).save()

        return redirect('dashboard')

    else:
        return redirect('dashboard')







