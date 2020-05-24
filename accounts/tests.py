from django.test import TestCase, Client
from accounts.models import Account
from projects.models import Workspace, Project
from tasks.models import Task, Cycle
from board.constants import *
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import timezone

# Create your tests here.


class AccountTest(TestCase):
    def setUp(self):
        self.existing_user = User.objects.create_user(username = 'email@email.com',password='123', email = 'email@email.com', first_name = 'Name', last_name='Last')
        create_mock_data('email@email.com')
        self.client = Client()

    def test_register_success(self):
        register_response = self.client.post('/accounts/register', {
            REGISTER_FORM_FIRST_NAME : 'jimmy',
            REGISTER_FORM_LAST_NAME : 'blue',
            REGISTER_FORM_EMAIL : 'jimmy@blue.com',
            REGISTER_FORM_PASSWORD : 'dlfkgj28',
            REGISTER_FORM_PASSWORD2 : 'dlfkgj28'
        })
        self.assertEqual(register_response.status_code,302)
        self.assertEqual(register_response.url,'/accounts/dashboard')
        account_created = Account.objects.filter(username = 'jimmy@blue.com')[0]
        workspace_created = Workspace.objects.filter(account=account_created)[0]
        project_created = Project.objects.filter(workspace=workspace_created)
        default_cycle_created = Cycle.objects.filter(workspace=workspace_created)
        self.assertTrue(account_created)
        self.assertTrue(workspace_created)
        self.assertTrue(project_created)
        self.assertTrue(default_cycle_created)

    def test_register_failed_if_different_passwords(self):
        register_response = self.client.post('/accounts/register', {
                REGISTER_FORM_FIRST_NAME : 'jimmy',
                REGISTER_FORM_LAST_NAME : 'blue',
                REGISTER_FORM_EMAIL : 'jimmy@blue.com',
                REGISTER_FORM_PASSWORD : 'different',
                REGISTER_FORM_PASSWORD2 : 'dlfkgj28'
        })
        self.assertEqual(register_response.status_code,302)
        self.assertEqual(register_response.url,'/accounts/register')

    def test_login_success(self):

        login_response = self.client.post('/accounts/login', {
            LOGIN_FORM_EMAIL_FIELD_NAME : 'email@email.com',
            LOGIN_FORM_PASSWORD_FIELD_NAME: '123'
        })
        self.assertEqual(login_response.status_code,302)
        self.assertEqual(login_response.url,'/accounts/dashboard')

    def test_login_failed_if_incorrect_password(self):

        login_response = self.client.post('/accounts/login', {
            LOGIN_FORM_EMAIL_FIELD_NAME : 'email@email.com',
            LOGIN_FORM_PASSWORD_FIELD_NAME: '1234'
        })
        self.assertEqual(login_response.status_code,302)
        self.assertEqual(login_response.url,'/accounts/login')

    def test_login_failed_if_user_doesnt_exist(self):

        login_response = self.client.post('/accounts/login', {
            LOGIN_FORM_EMAIL_FIELD_NAME : 'email2@email.com',
            LOGIN_FORM_PASSWORD_FIELD_NAME: '1234'
        })
        self.assertEqual(login_response.status_code,302)
        self.assertEqual(login_response.url,'/accounts/login')

    def test_dashboard_success_check_context(self):
        login_response = self.client.post('/accounts/login', {
            LOGIN_FORM_EMAIL_FIELD_NAME : 'email@email.com',
            LOGIN_FORM_PASSWORD_FIELD_NAME: '123'
        })
        self.assertEqual(login_response.status_code,302)
        dashboard_response =self.client.get('/accounts/dashboard')
        self.assertEqual(dashboard_response.status_code, 200)
        self.assertTrue( 'tasks_grouped_by_status' in dashboard_response.context)
        self.assertTrue( 'board_progress_summary' in dashboard_response.context)
        self.assertTrue( 'projects' in dashboard_response.context)
        self.assertTrue( 'cycle' in dashboard_response.context)
        self.assertEqual([project.title for project in dashboard_response.context['projects']],['Project 1','Project 2'])
        self.assertEqual([dashboard_response.context['board_progress_summary']['total_tasks']],[4])
        self.assertEqual([dashboard_response.context['board_progress_summary']['completed_percentage']],[25])
        self.assertEqual([dashboard_response.context['board_progress_summary']['completed_tasks']],[1])
        self.assertEqual(len(dashboard_response.context['tasks_grouped_by_status']),4)

        for tasks_group in dashboard_response.context['tasks_grouped_by_status']:
            if(tasks_group['status'] == 'OPEN'):
                self.assertEqual(tasks_group['tasks'][0].title,'task 1')
            if(tasks_group['status'] == 'READY'):
                self.assertEqual(tasks_group['tasks'][0].title,'task 2')
            if(tasks_group['status'] == 'IN_PROGRESS'):
                self.assertEqual(tasks_group['tasks'][0].title,'task 3')
            if(tasks_group['status'] == 'DONE'):
                self.assertEqual(tasks_group['tasks'][0].title,'task 4')

    def test_dashboard_cycle_is_received(self):
        login_response = self.client.post('/accounts/login', {
            LOGIN_FORM_EMAIL_FIELD_NAME : 'email@email.com',
            LOGIN_FORM_PASSWORD_FIELD_NAME: '123'
        })
        self.assertEqual(login_response.status_code,302)
        dashboard_response =self.client.get('/accounts/dashboard')
        self.assertTrue( 'cycle' in dashboard_response.context)
        self.assertEqual(dashboard_response.context['cycle'].goal_title,'Active')





def create_mock_data(email):
    account = Account(username=email,email = email)
    account.save()
    workspace= Workspace(account= account)
    workspace.save()
    project1= Project(title = 'Project 1', description='Project1 description', workspace = workspace, color='#ffffff')
    project1.save()
    task1 = Task(title='task 1' ,description= 'task 1 description', project= project1, estimated_hours= 1, status='OPEN',workspace=workspace, assigned_user=account)
    task1.save()
    task2 = Task(title='task 2' ,description= 'task 2 description', project= project1, estimated_hours= 1, status='READY',workspace=workspace, assigned_user=account)
    task2.save()
    project2= Project(title = 'Project 2', description='Project2 description', workspace = workspace, color='#ffff00')
    project2.save()
    task3 = Task(title='task 3' ,description= 'task 3 description', project= project2, estimated_hours= 1, status='IN_PROGRESS',workspace=workspace, assigned_user=account)
    task3.save()
    task4 = Task(title='task 4' ,description= 'task 4 description', project= project2, estimated_hours= 1, status='DONE',workspace=workspace, assigned_user=account)
    task4.save()
    tasks = Task.objects.all()
    cycle = Cycle(goal_title='Default', start_date=timezone.now(), workspace=workspace)
    cycle.save()
    activeCycle = Cycle(goal_title='Active', start_date=timezone.now(),end_date=timezone.now()+ timezone.timedelta(7), workspace=workspace)
    activeCycle.save()
    activeCycle.tasks.set(tasks)
    cycle.save()






