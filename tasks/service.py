from projects.models import Project, Workspace
from accounts.models import Account
from tasks.models import Task, get_active_cycle

def save_or_update_task(task_form, workspace_id):
    project = Project.objects.filter(id=task_form.projectId)[0]
    account = Account.objects.filter(username=task_form.assignedPerson)[0]

    if(not project):
        project = Project.objects.filter(title='Default')[0]

    if(task_form.taskId):
        # update it
        task = Task.objects.filter(id=task_form.taskId)[0]
        task.title=task_form.titleName
        task.description= task_form.description
        task.estimated_hours= task_form.estimatedHours
        task.assigned_user = account
        task.status=task_form.status
        task.project=project
        task.save()

    else:
        # create it
        workspace = Workspace.objects.filter(id= workspace_id)[0]
        task = Task(title=task_form.titleName,description= task_form.description,
                    estimated_hours= task_form.estimatedHours,status=task_form.status, project=project,assigned_user=account, workspace=workspace)
        task.save()
        if(task_form.include_to_current_cycle == 'on'):
            cycle = get_active_cycle(workspace_id)
            cycle.tasks.add(task)

def remove_task(taskId, workspaceId):
    Task.objects.filter(id=taskId).delete()