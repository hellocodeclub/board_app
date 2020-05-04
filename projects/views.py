from django.shortcuts import render,redirect
from projects.models import Project
from tasks.models import Task

# Create your views here.

def projects(request):
    context = {
        'projects':get_projects_with_their_tasks()
    }
    return render(request, 'projects/projects.html', context)

def reports(request):
    return render(request, 'projects/reports.html')


def get_projects_with_their_tasks():
    projects_with_their_tasks = []
    projects = Project.objects.all()
    for project in projects:
        tasks = Task.objects.filter(project=project)
        project_with_tasks = {
            'project': project,
            'tasks': tasks
        }
        projects_with_their_tasks.append(project_with_tasks)
    return projects_with_their_tasks
