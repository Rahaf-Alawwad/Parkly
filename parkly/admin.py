from django.contrib import admin
from .models import Profile, Lot,Parking,Reservation
# Register your models here.
admin.site.register(Profile)
admin.site.register(Lot)
admin.site.register(Parking)
admin.site.register(Reservation)


