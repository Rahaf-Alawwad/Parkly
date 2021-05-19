from django.forms import ModelForm
from .models import Measurement, SiteRequests, Lot

class RequestForm(ModelForm):

    class Meta:
        model = SiteRequests
        fields = '__all__'


class RegisterBusinessForm(ModelForm):

    class Meta:
        model = Lot
        fields = ('name','location','image','available_parking',)


class mapForm(ModelForm):

    class Meta:
        model = Measurement
        fields =('destination',)