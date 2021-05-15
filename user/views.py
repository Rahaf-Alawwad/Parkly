# from django.shortcuts import redirect, render
# from .forms import UserForm
# from Zeta_project.settings import EMAIL_HOST_USER
# from django.core.mail import send_mail
# # Create your views here.

# def register(request):
#     form = UserForm()
#     if(request.method == "POST"):
#         user =  UserForm(request.POST)
#         subject = 'Welcome to Parkly'
#         message = 'Welcome, '+str(user['first_name'].value())
#         recepient = str(user['email'].value())
#         send_mail(subject, 
#             message, EMAIL_HOST_USER, [recepient], fail_silently = False)
#         if (user.is_valid()):
#             user.save()
#             return redirect('/')
#         else:
#             print(user.errors)
#     return render(request, "register.html", {"form":form})
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate , logout
from user.forms import RegistrationForm, UserAuthForm
from user.models import User

def signup_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            # email = form.cleaned_data.get('email')
            # first_name = form.cleaned_data.get('first_name')
            # last_name = form.cleaned_data.get('last_name')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
           
            login(request, user)
            return redirect('home')
        else:
            context['registration_form'] = form
    else: #GET request
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'signup.html', context)

def login_view(request):

    context = {}
    user =request.user
    if user.is_authenticated:
        return redirect('home')
    
    if request.POST:
        form =UserAuthForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate( username='admin', password="admin" )

            if user:
                login(request, user)
                return redirect('home')

    else:
        form = UserAuthForm()
    
    context['login_form'] = form
    return render(request, 'login.html', context)

def profile_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        context['profile'] = get_object_or_404(User, username=user)
        return render(request, 'profile.html', context)
    return redirect('login')

def logout_view(request):
    logout(request)
    return redirect('home')