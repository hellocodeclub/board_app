from django.shortcuts import render
from django.http import HttpResponse
from tasks.models import Task, get_dictionary_tasks_by_status, calculate_completed_hours
from tasks.choices import status_choices


def index(request):
    tasks_groups = get_dictionary_tasks_by_status()
    board_progress_summary = calculate_completed_hours()
    context = {
        'tasks_grouped_by_status': tasks_groups,
        'board_progress_summary': board_progress_summary,

    }
    print(context)
    return render(request,'pages/index.html', context)