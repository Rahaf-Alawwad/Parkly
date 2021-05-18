import django_filters
from .models import *

class LotFilter(django_filters.FilterSet):
    class Meta:
        model= Lot
        fields= ("name","location")

