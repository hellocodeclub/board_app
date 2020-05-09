from django.contrib import admin
from .models import Project, Workspace
# Register your models here.

class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('id','account')
    #list_display_links = ('id'),


admin.site.register(Project)
admin.site.register(Workspace,WorkspaceAdmin)