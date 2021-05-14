from django import forms
from .models import SiteRequests

class RequestForm(forms.ModelForm):

    class Meta:
        model = SiteRequests
        fields = '__all__'