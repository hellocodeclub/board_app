from django.shortcuts import render,redirect
from tasks.models import Task, get_list_tasks_by_status, calculate_completed_hours, get_active_cycle
from tasks.choices import status_choices
from django.contrib import messages, auth
from .domain import AccountRegistration,create_session
from django.contrib.auth.models import User
from projects.models import Project
from board.constants import *
from django.contrib.auth.decorators import login_required

# Create your views here.

def login(request):
    if request.method == 'POST':
        email = request.POST[LOGIN_FORM_EMAIL_FIELD_NAME]
        password = request.POST[LOGIN_FORM_PASSWORD_FIELD_NAME]
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request,'You are now logged in')
            create_session(request, email)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request,'accounts/login.html')

def register(request):
    if request.method == 'POST':
        registration = AccountRegistration(request)
        registrationResult_Tuple_with_BooleanAndMessage = registration.checkIfValid_and_returnMessage()
        if(registrationResult_Tuple_with_BooleanAndMessage[0]):
            user= User.objects.create_user(username=registration.email, password=registration.password,
                                           email=registration.email, first_name=registration.first_name,last_name=registration.last_name)
            registration.register(request, user)
            messages.success(request, registrationResult_Tuple_with_BooleanAndMessage[1])
            create_session(request, registration.email)
            return redirect('dashboard')
        else:
            messages.error(request, registrationResult_Tuple_with_BooleanAndMessage[1])
            return redirect('register')
    else:
        return render(request,'accounts/register.html')

def logout(request):
    if request.method =='POST':
        auth.logout(request)
        request.session.clear()
        messages.success(request,'You are now logged out')
        return redirect('index')

@login_required(login_url='login')
def dashboard(request):
    if request.user.is_authenticated:

        workspace_id = request.session.get(SESSION_WORKSPACE_KEY_NAME)
        tasks_groups = get_list_tasks_by_status(workspace_id)
        board_progress_summary = calculate_completed_hours()
        projects = Project.objects.all()
        activate_cycle = get_active_cycle(workspace_id)
        context = {
            CONTEXT_DASHBOARD_TASK_GROUPS_BY_STATUS_FIELD: tasks_groups,
            CONTEXT_DASHBOARD_PROGRESSBAR_FIELD: board_progress_summary,
            CONTEXT_PROJECT_FIELD: projects,
            CONTEXT_GOAL_TITLE: activate_cycle.goal_title
        }
        return render(request,'accounts/dashboard.html', context)
    else:
        return redirect('index')
