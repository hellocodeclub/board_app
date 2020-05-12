from django.contrib.auth.models import User
from .models import Account
from projects.models import Workspace,Project
from django.contrib import auth
from board.constants import SESSION_WORKSPACE_KEY_NAME,REGISTER_FORM_FIRST_NAME,REGISTER_FORM_EMAIL,REGISTER_FORM_LAST_NAME,REGISTER_FORM_PASSWORD,REGISTER_FORM_PASSWORD2

class AccountRegistration:
    def __init__(self,request):
        self.first_name = request.POST[REGISTER_FORM_FIRST_NAME]
        self.last_name= request.POST[REGISTER_FORM_LAST_NAME]
        self.email = request.POST[REGISTER_FORM_EMAIL]
        self.password = request.POST[REGISTER_FORM_PASSWORD]
        self.password2 = request.POST[REGISTER_FORM_PASSWORD2]

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

def create_session(request, username):
    account = Account.objects.filter(username=username)[0]
    workspace = Workspace.objects.filter(account=account)[0]
    request.session.set_expiry(3000) # 50 minutes
    request.session[SESSION_WORKSPACE_KEY_NAME] = workspace.id





