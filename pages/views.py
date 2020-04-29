from django.shortcuts import render
from django.http import HttpResponse
from tasks.models import Task, get_dictionary_tasks_by_status

def index(request):
    tasks_groups = get_dictionary_tasks_by_status()
    context = {
        'task_groups': tasks_groups
    }
    print(context)
    return render(request,'pages/index.html', context)