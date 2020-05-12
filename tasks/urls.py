from django.urls import path
from . import views

urlpatterns = [
    path('task-move-next-state', views.task_next_state, name='task-move-next-state'),
    path('task-increase-priority', views.task_increase_priority, name='task-increase-priority'),
    path('save-task', views.save_task, name='save-task'),
    path('tasks', views.tasks, name='tasks')
]