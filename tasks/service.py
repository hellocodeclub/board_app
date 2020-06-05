from projects.models import Project, Workspace
from accounts.models import Account
from tasks.models import Task, get_active_cycle, get_tasks_on_board, get_default_cycle, CycleHistoryData
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils import timezone

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


def end_activate_cycle(workspaceId):
    # get the active cycle and all not done task
    all_tasks_on_board = get_tasks_on_board(workspaceId)
    total_hours_in_cycle = all_tasks_on_board.aggregate(hours=Coalesce(Sum('estimated_hours'),0))
    finished_hours = all_tasks_on_board.filter(status='DONE').aggregate(hours=Coalesce(Sum('estimated_hours'),0))
    tasks_on_the_board_not_finished=all_tasks_on_board.exclude(status='DONE')

    # Move unfinished tasks to the default cycle
    default_cycle=get_default_cycle(workspaceId)
    for not_finished_task in tasks_on_the_board_not_finished:
        default_cycle.tasks.add(not_finished_task)
        default_cycle.save()

    # Close the active cycle
    active_cycle = get_active_cycle(workspaceId)
    active_cycle.end_date = timezone.now()
    active_cycle.save()

    workspace = Workspace.objects.filter(id= workspaceId)[0]

    #Calculate cycle duration
    cycle_duration = timezone.now() - active_cycle.start_date
    # Create the cycle history entry
    cycle_history_entry = CycleHistoryData(start_date=active_cycle.start_date, end_date=timezone.now(),
                                           workspace=workspace,
                                           duration=cycle_duration, planned_hours=total_hours_in_cycle.get('hours'),
                                           done_hours=finished_hours.get('hours'))
    cycle_history_entry.save()
