from django.urls import path
from . import views

urlpatterns = [
    path('task-move-next-state', views.task_next_state, name='task-move-next-state')
]