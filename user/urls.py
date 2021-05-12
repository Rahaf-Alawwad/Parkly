from django.urls import path 
from django.contrib.auth import views as as_view

urlpatterns = [
    path('login/', as_view.LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', as_view.LoginView.as_view(), name="logout")

]