# from django import forms 
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
# from parkly.models import Profile

# class UserForm(UserCreationForm):
  
#     class Meta:
        
#         model = User
#         fields = ("username","first_name","last_name","email")


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from .models import User


class RegistrationForm(UserCreationForm):
    username        = forms.CharField( max_length=20, help_text='Required. Add a valid username' )
    first_name        = forms.CharField(max_length=20, help_text='Required. Add a valid first name')
    last_name        = forms.CharField( max_length=20, help_text='Required. Add a valid last name')
    email           = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')
  
    
    class Meta:
        model = User
        fields = ('username', 'first_name','last_name','email','password1', 'password2')


class UserAuthForm(forms.ModelForm):
    password = forms.CharField(label='Password' , widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields= ('username' , 'password')

    def clean(self):
        if self.is_valid():
            username= self.cleaned_data['username']
            password= self.cleaned_data['password']
            if not authenticate(username=username,password=password):
                raise forms.ValidationError("Invalid login")