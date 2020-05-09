from django.shortcuts import render,redirect
from tasks.models import Task, get_dictionary_tasks_by_status, calculate_completed_hours
from tasks.choices import status_choices
from django.contrib import messages, auth
from .domain import AccountRegistration,create_session
from django.contrib.auth.models import User
from projects.models import Project
from board.constants import LOGIN_FORM_EMAIL_FIELD_NAME, LOGIN_FORM_PASSWORD_FIELD_NAME

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

def dashboard(request):
    if request.user.is_authenticated:
        tasks_groups = get_dictionary_tasks_by_status()
        board_progress_summary = calculate_completed_hours()
        projects = Project.objects.all()
        context = {
            'tasks_grouped_by_status': tasks_groups,
            'board_progress_summary': board_progress_summary,
            'projects': projects

        }
        return render(request,'accounts/dashboard.html', context)
    else:
        return redirect('index')
