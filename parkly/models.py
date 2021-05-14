from django.db import models
from datetime import datetime,date,time

from user.models import User

# Create your models here.
choices = (
    ('owner'  , 'owner'),
    ('user' , 'user')
    )

##


class Profile(models.Model):
    #image = models.ImageField(upload_to ="img/" , null=True)
    name=models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    user = models.OneToOneField(User , related_name="profile" , on_delete=models.CASCADE)
    user_type = models.CharField( max_length=255, choices=choices , null=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    contact_number = models.CharField(max_length=12)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name
  

class Lot(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True)
    image = models.CharField(max_length=255, null=True)
    available_parking = models.PositiveIntegerField(null=False)
    owner = models.OneToOneField(Profile , related_name="owner" ,on_delete=models.CASCADE, null=True) ## each lot has one owner

    def __str__(self):
        return self.name

class Parking(models.Model):

    lot = models.ForeignKey(Lot , related_name="lot" ,on_delete=models.CASCADE, null=True) ## each parking has one lot
    park_ID = models.CharField(max_length=4, null=True)
    available = models.BooleanField(default=True)
    is_reentry_allowed = models.BooleanField(null=True)
    price =  models.DecimalField(max_digits=10,null=False,decimal_places=2)
   
    def __str__(self):
        return self.park_ID


class Reservation(models.Model):
    date=models.DateField(null=True)
    reservation_date=models.DateField(null=True)
    timeFrom = models.TimeField(null=True)
    timeTo = models.TimeField(null=True)
    code = models.CharField(max_length=10, unique=True)
    #duration =  models.PositiveIntegerField(default=1)
    cost= models.PositiveIntegerField(null=False)
    is_paid = models.BooleanField(default=False)
    user = models.ForeignKey(Profile , related_name="profile" ,on_delete=models.CASCADE, null=True) ## user might have more than one reservation
    parking = models.ForeignKey(Parking , related_name="parking" ,on_delete=models.CASCADE, null=True) ## each parking has many reservation

    def __str__(self):
        return self.code


