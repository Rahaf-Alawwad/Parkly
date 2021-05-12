from django.urls import path
from django.contrib.auth import views as as_view
from user import views as user_views

urlpatterns = [
    path('login/' , user_views.login_view ,name="login"),
    path('logout/' , user_views.logout_view , name= "logout"), 
    path('signup/' , user_views.signup_view ,name="signup"), 
    path('profile/' , user_views.profile_view ,name="profile")
    
]