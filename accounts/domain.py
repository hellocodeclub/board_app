from django.contrib.auth.models import User

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


