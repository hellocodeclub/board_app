from django.test import TestCase
from tasks.models import Task, get_active_cycle
from accounts.tests import create_mock_data
from django.contrib.auth.models import User
from projects.models import Project, Workspace
from board.constants import *

# Create your tests here.

class TaskTest(TestCase):
    def setUp(self):
        self.existing_user = User.objects.create_user(username = 'email@email.com',password='123', email = 'email@email.com', first_name = 'Name', last_name='Last')
        # task 1 is in open state
        create_mock_data('email@email.com')

    def test_task_next_state_success(self):
        login_response = self.client.post('/accounts/login', {
            LOGIN_FORM_EMAIL_FIELD_NAME : 'email@email.com',
            LOGIN_FORM_PASSWORD_FIELD_NAME: '123'
        })
        self.assertEqual(login_response.status_code,302)
        task_updated = Task.objects.all()[0]
        next_state_response = self.client.post(path='/tasks/task-move-next-state', data={'task-id': task_updated.id})
        self.assertEqual(next_state_response.status_code, 302)
        self.assertEqual(next_state_response.url,'/accounts/dashboard')
        task_updated = Task.objects.filter(description= task_updated.description)[0]
        self.assertEqual(task_updated.status, 'READY')

    def test_task_next_state_failed_if_not_authenticated(self):
        login_response = self.client.post('/accounts/logout', {
                LOGIN_FORM_EMAIL_FIELD_NAME : 'email@email.com',
                LOGIN_FORM_PASSWORD_FIELD_NAME: '1234'
        })
        self.assertEqual(login_response.status_code,302)
        next_state_response = self.client.post(path='/tasks/task-move-next-state', data={'task-id':1})
        self.assertEqual(next_state_response.status_code, 302)
        self.assertEqual(next_state_response.url,'/accounts/login?next=/tasks/task-move-next-state')

        increase_priority_response = self.client.post(path='/tasks/task-increase-priority', data={'task-id': 1})
        self.assertEqual(increase_priority_response.status_code, 302)
        self.assertEqual(increase_priority_response.url,'/accounts/login?next=/tasks/task-increase-priority')

        get_tasks_response = self.client.post(path='/tasks/tasks', data={'task-id': 1})
        self.assertEqual(get_tasks_response.status_code, 302)
        self.assertEqual(get_tasks_response.url,'/accounts/login?next=/tasks/tasks')


    def test_task_increase_priority(self):
        login_response = self.client.post('/accounts/login', {
            LOGIN_FORM_EMAIL_FIELD_NAME : 'email@email.com',
            LOGIN_FORM_PASSWORD_FIELD_NAME: '123'
        })
        self.assertEqual(login_response.status_code,302)
        task_not_updated = Task.objects.all()[0]
        increase_priority_response = self.client.post(path='/tasks/task-increase-priority', data={'task-id': task_not_updated.id})
        self.assertEqual(increase_priority_response.status_code, 302)
        self.assertEqual(increase_priority_response.url,'/accounts/dashboard')
        task_updated = Task.objects.filter(description= task_not_updated.description)[0]
        self.assertEqual(task_not_updated.priority+1, task_updated.priority)

    def test_save_new_task(self):
        login_response = self.client.post('/accounts/login', {
            LOGIN_FORM_EMAIL_FIELD_NAME : 'email@email.com',
            LOGIN_FORM_PASSWORD_FIELD_NAME: '123'
        })
        self.assertEqual(login_response.status_code,302)
        existing_project = Project.objects.all()[0]
        data={
            TASK_FORM_NAME: 'Do something cool',
            TASK_FORM_DESCRIPTION : 'Do something cool',
            TASK_FORM_STATUS:'OPEN',
            TASK_FORM_ESTIMATED_HOURS: 1,
            TASK_FORM_PROJECT: existing_project.id,
            TASK_FORM_ASSIGNED_PERSON: 'email@email.com'

        }
        save_task_response = self.client.post(path='/tasks/save-task', data=data)
        self.assertEqual(save_task_response.status_code, 302)
        task_created = Task.objects.filter(description= data[TASK_FORM_DESCRIPTION])[0]
        self.assertTrue(task_created)

    def test_new_task_added_to_active_cycle(self):
        login_response = self.client.post('/accounts/login', {
                LOGIN_FORM_EMAIL_FIELD_NAME : 'email@email.com',
                LOGIN_FORM_PASSWORD_FIELD_NAME: '123'
        })
        self.assertEqual(login_response.status_code,302)
        existing_project = Project.objects.all()[0]
        existing_workspace = Workspace.objects.all()[0]
        data={
            TASK_FORM_NAME: 'Do something cool',
            TASK_FORM_DESCRIPTION : 'Do something cool',
            TASK_FORM_STATUS:'OPEN',
            TASK_FORM_ESTIMATED_HOURS: 1,
            TASK_FORM_PROJECT: existing_project.id,
            TASK_FORM_ASSIGNED_PERSON: 'email@email.com',
            TASK_FORM_INCLUDE_IN_CURRENT_CYCLE: 'on'

        }
        save_task_response = self.client.post(path='/tasks/save-task', data=data)
        self.assertEqual(save_task_response.status_code, 302)
        task_created = Task.objects.filter(description= data[TASK_FORM_DESCRIPTION])[0]
        self.assertTrue(task_created)
        cycle = get_active_cycle(existing_workspace.id)
        self.assertTrue(cycle.tasks.filter(id=task_created.id))

    def test_update_task(self):
        login_response = self.client.post('/accounts/login', {
            LOGIN_FORM_EMAIL_FIELD_NAME : 'email@email.com',
            LOGIN_FORM_PASSWORD_FIELD_NAME: '123'
        })
        self.assertEqual(login_response.status_code,302)
        existing_task = Task.objects.all()[0]
        data={
            TASK_FORM_ID: existing_task.id,
            TASK_FORM_NAME: 'Do something cool',
            TASK_FORM_DESCRIPTION : 'Do something cool',
            TASK_FORM_STATUS:existing_task.status,
            TASK_FORM_ESTIMATED_HOURS: existing_task.estimated_hours,
            TASK_FORM_PROJECT: existing_task.project.id,
            TASK_FORM_ASSIGNED_PERSON: existing_task.assigned_user.username

        }
        save_task_response = self.client.post(path='/tasks/save-task', data=data)
        self.assertEqual(save_task_response.status_code, 302)
        task_created = Task.objects.filter(id= existing_task.id)[0]
        self.assertTrue(task_created)
        self.assertEqual(task_created.title, data.get(TASK_FORM_NAME))
        self.assertEqual(task_created.description, data.get(TASK_FORM_DESCRIPTION))

    def test_delete_task(self):
        login_response = self.client.post('/accounts/login', {
            LOGIN_FORM_EMAIL_FIELD_NAME : 'email@email.com',
            LOGIN_FORM_PASSWORD_FIELD_NAME: '123'
        })
        self.assertEqual(login_response.status_code,302)
        existing_task = Task.objects.all()[0]
        number_existing_tasks = Task.objects.all().count()
        data={
            TASK_FORM_ID: existing_task.id
        }
        save_task_response = self.client.post(path='/tasks/delete-task', data=data)
        self.assertEqual(save_task_response.status_code, 302)
        number_existing_tasks_after_deletion = Task.objects.all().count()
        self.assertEqual(number_existing_tasks-1, number_existing_tasks_after_deletion)
















