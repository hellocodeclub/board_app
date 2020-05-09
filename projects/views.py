from django.shortcuts import render,redirect
from projects.models import Project
from tasks.models import Task, caclulate_status_percentages
from board.constants import SESSION_WORKSPACE_KEY_NAME

# Create your views here.

def projects(request):
    workspace_id = request.session.get(SESSION_WORKSPACE_KEY_NAME)

    context = {
        'projects':get_projects_with_their_tasks(workspace_id)
    }
    return render(request, 'projects/projects.html', context)

def reports(request):
    return render(request, 'projects/reports.html')


def get_projects_with_their_tasks(workspace_id):
    projects_with_their_tasks = []
    projects = Project.objects.filter(workspace= workspace_id)

    for project in projects:
        tasks = Task.objects.filter(project=project)
        percentages_per_status = caclulate_status_percentages(project)
        project_with_tasks = {
            'project': project,
            'tasks': tasks,
            'status':percentages_per_status
        }
        projects_with_their_tasks.append(project_with_tasks)
    return projects_with_their_tasks

