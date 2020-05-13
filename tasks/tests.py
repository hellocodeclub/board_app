from django.test import TestCase
from tasks.models import Task
from accounts.tests import create_mock_data
from django.contrib.auth.models import User
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








