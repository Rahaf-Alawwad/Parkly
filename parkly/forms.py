from django.forms import ModelForm
from .models import SiteRequests, Lot

class RequestForm(ModelForm):

    class Meta:
        model = SiteRequests
        fields = '__all__'


class RegisterBusinessForm(ModelForm):

    class Meta:
        model = Lot
        fields = '__all__'