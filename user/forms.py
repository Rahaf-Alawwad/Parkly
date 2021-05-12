from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from user.models import User


class RegistrationForm(UserCreationForm):
    username        = forms.CharField( max_length=20, help_text='Required. Add a valid username' )
    first_name        = forms.CharField(max_length=20, help_text='Required. Add a valid first name')
    last_name        = forms.CharField( max_length=20, help_text='Required. Add a valid last name')
    email           = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')
    img           = forms.CharField(max_length=1000,help_text='Required. Add a valid profile imgae url')
    
    class Meta:
        model = User
        fields = ('username', 'first_name','last_name','email', 'img','password1', 'password2')


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
        