from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
choices = (
    ('owner'  , 'owner'),
    ('user' , 'user')
    )


class Profile(models.Model):
    #image = models.ImageField(upload_to ="img/" , null=True)
    name=models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    user = models.OneToOneField(User , related_name="profile" , on_delete=models.CASCADE)
    user_type = models.CharField( max_length=255, choices=choices , null=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    contact_number = models.CharField(max_length=12)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return self.name



class Lot(models.Model):
    name = models.CharField(max_length=255)
    available_parking = models.PositiveIntegerField(null=False)
    owner = models.OneToOneField(Profile , related_name="owner" ,on_delete=models.CASCADE, null=True) ## each lot has one owner

    def __str__(self):
        return self.name



class Parking(models.Model):

    lot = models.ForeignKey(Lot , related_name="lot" ,on_delete=models.CASCADE, null=True) ## each parking has one lot
    park_ID = models.CharField(max_length=4, null=True, unique=True)
    location = models.CharField(max_length=255, null=True)
    available = models.BooleanField(default=True)
    is_reentry_allowed = models.BooleanField(null=True)
    price =  models.DecimalField(null=False)
   
    def __str__(self):
        return self.parkID



class Reservation(models.Model):
    dateTime = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=10, unique=True)
    duration =  models.PositiveIntegerField(default=1)
    cost= models.PositiveIntegerField(null=False)
    is_paid = models.BooleanField(default=False)
    user = models.ForeignKey(Profile , related_name="user" ,on_delete=models.CASCADE, null=True) ## user might have more than one reservation
    parking = models.OneToOneField(Parking , related_name="parking" ,on_delete=models.CASCADE, null=True) ## each parking has one reservation

    def __str__(self):
        return self.code


