from django.forms import ModelForm
from .models import SiteRequests

class RequestForm(ModelForm):

    class Meta:
        model = SiteRequests
        fields = '__all__'