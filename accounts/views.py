from django.shortcuts import render,redirect
from tasks.models import Task, get_dictionary_tasks_by_status, calculate_completed_hours
from tasks.choices import status_choices
from django.contrib import messages, auth
from .domain import AccountRegistration
from django.contrib.auth.models import User

# Create your views here.

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request,'You are now logged in')
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
            auth.login(request, user)
            messages.success(request, registrationResult_Tuple_with_BooleanAndMessage[1])
            return redirect('dashboard')
        else:
            messages.error(request, registrationResult_Tuple_with_BooleanAndMessage[1])
            return redirect('register')
    else:
        return render(request,'accounts/register.html')

def logout(request):
    return redirect('index')

def dashboard(request):
    tasks_groups = get_dictionary_tasks_by_status()
    board_progress_summary = calculate_completed_hours()
    context = {
        'tasks_grouped_by_status': tasks_groups,
        'board_progress_summary': board_progress_summary,

    }
    return render(request,'accounts/dashboard.html', context)
