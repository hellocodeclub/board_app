from django.urls import path
from . import views

urlpatterns = [
    path('task-move-next-state', views.task_next_state, name='task-move-next-state'),
    path('task-increase-priority', views.task_increase_priority, name='task-increase-priority'),
    path('save-task', views.save_task, name='save-task'),
    path('delete-task', views.delete_task, name='delete-task'),
    path('start-cycle', views.start_cycle, name='start-cycle'),
    path('create_notification', views.create_notification, name='create_notification'),
    path('tasks', views.tasks, name='tasks')
]