from django.shortcuts import render, redirect
from tasks.models import Task
from tasks.choices import next_state

# Create your views here.

def task_next_state(request):
    if (request.method == 'POST'):
        task_id = request.POST['task_id']
        task_to_update = Task.objects.filter(id=task_id)
        if(task_to_update):
            next_status=next_state(task_to_update.values('status')[0]['status'])
            task_to_update.update(status=next_status)
        return redirect('dashboard')
    else:
        return render(request, 'accounts/dashboard.html')
