from django.contrib import admin
from .models import  Lot,Parking,Reservation,SiteRequests,Measurement
# Register your models here.

admin.site.register(Lot)
admin.site.register(Parking)
admin.site.register(Reservation)
admin.site.register(SiteRequests)
admin.site.register(Measurement)


