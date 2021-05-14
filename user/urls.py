from django.urls import path
from user import views 
from django.contrib.auth import views as as_view
from user import views 

urlpatterns = [
    path('login/', as_view.LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', as_view.LogoutView.as_view(), name="logout"),
    path('register/', views.register, name="register"),
    path('resetPassword/',as_view.PasswordResetView.as_view(template_name="reset_password.html"), name="password_reset"),
    path('resetPasswordSent/',as_view.PasswordChangeDoneView.as_view(), name="password_reset_done"),
    path('password/reset/confirm/<uidb64>/<token>/', as_view.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('resetPasswordComplete/',as_view.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
<<<<<<< HEAD

=======
 
>>>>>>> fd43be66f414c4a9aaffad6fa635f1d4a71f3673
]