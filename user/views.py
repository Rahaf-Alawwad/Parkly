from django.shortcuts import redirect, render
from .forms import UserForm
from Zeta_project.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
# Create your views here.

def register(request):
    form = UserForm()
    if(request.method == "POST"):
        user =  UserForm(request.POST)
        subject = 'Welcome to Parkly'
        message = 'Welcome, '+str(user['first_name'].value())
        recepient = str(user['email'].value())
        send_mail(subject, 
            message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        if (user.is_valid()):
            user.save()
            return redirect('/home')
        else:
            print(user.errors)
    return render(request, "register.html", {"form":form})