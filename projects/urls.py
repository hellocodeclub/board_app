from django.urls import path
from . import views

urlpatterns = [
    path('projects', views.projects, name='projects'),
    path('save-project', views.save_project, name='save-project'),
    path('delete-project', views.delete_project, name ='delete-project'),
    path('reports', views.reports, name='reports')
]