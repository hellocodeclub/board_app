from django.contrib.auth.models import User
from .models import Account
from projects.models import Workspace,Project
from django.contrib import auth

class AccountRegistration:
    def __init__(self,request):
        self.first_name = request.POST['first_name']
        self.last_name= request.POST['last_name']
        self.email = request.POST['email']
        self.password = request.POST['password']
        self.password2 = request.POST['password2']

    def checkIfValid_and_returnMessage(self):
        if self.password != self.password2:
            return (False,'Passwords entered were different')
        else:
            if User.objects.filter(email=self.email).exists():
                return (False,'Email is being used')
            else:
                return (True,'You are now registered and can log in')

    def register(self, request, user):
        auth.login(request, user)
        account = Account(username=user.email, email=user.email)
        account.save()
        workspace = Workspace(account=account)
        workspace.save()
        default_project = Project(title='Default',description='',workspace=workspace,color='#FFFFFF')
        default_project.save()




