from django.shortcuts import render,redirect
from projects.models import Project, Workspace
from tasks.models import Task, caclulate_status_percentages
from board.constants import SESSION_WORKSPACE_KEY_NAME
from django.contrib.auth.decorators import login_required
from affilliateproducts.models import AffilliateProduct

# Create your views here.

@login_required(login_url='login')
def projects(request):
    workspace_id = request.session.get(SESSION_WORKSPACE_KEY_NAME)
    recommendations = AffilliateProduct.objects.all()

    context = {
        'projects':get_projects_with_their_tasks(workspace_id),
        'recommendations': recommendations
    }
    return render(request, 'projects/projects.html', context)

def reports(request):
    return render(request, 'projects/reports.html')

@login_required(login_url='login')
def save_project(request):
    workspace_id = request.session.get(SESSION_WORKSPACE_KEY_NAME)
    if(request.method == 'POST'):
        id = request.POST.get('project-id')
        title = request.POST.get('project-title')
        description = request.POST.get('project-description')
        color = request.POST.get('project-color')
        if(id):
            # update
            existing_project = Project.objects.filter(id=id)[0]
            existing_project.title = title
            existing_project.description = description
            existing_project.color = color
            existing_project.save()
        else:
            workspace = Workspace.objects.filter(id= workspace_id)[0]
            new_project = Project(title=title, description=description, color=color, workspace= workspace)
            new_project.save()

        return redirect('projects')
    else:
        return redirect('projects')


@login_required(login_url='login')
def delete_project(request):
    if(request.method == 'POST'):
        project_id= request.POST.get('project-id')
        workspace_id = request.session.get(SESSION_WORKSPACE_KEY_NAME)
        Project.objects.filter(id=project_id).delete()
        return redirect('projects')

    else:
        return redirect('projects')



def get_projects_with_their_tasks(workspace_id):
    projects_with_their_tasks = []
    projects = Project.objects.filter(workspace= workspace_id).order_by('-updated_at')

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

