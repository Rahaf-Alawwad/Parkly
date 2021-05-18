from django.urls import path
from user import views 
from django.contrib.auth import views as as_view
from user import views 

urlpatterns = [
    path('login/' , views.login_view ,name="login"),
    path('logout/' , views.logout_view , name= "logout"), 
    path('signup/' , views.signup_view ,name="signup"), 
    path('resetPassword/',as_view.PasswordResetView.as_view(template_name="reset_password.html"), name="password_reset"),
    path('resetPasswordSent/',as_view.PasswordChangeDoneView.as_view(template_name="reset_password.html"), name="password_reset_done"),
    path('password/reset/confirm/<uidb64>/<token>/', as_view.PasswordResetConfirmView.as_view(template_name="reset_password.html"), name='password_reset_confirm'),
    path('resetPasswordComplete/',as_view.PasswordResetCompleteView.as_view(template_name="reset_password.html"),name="password_reset_complete"),
]