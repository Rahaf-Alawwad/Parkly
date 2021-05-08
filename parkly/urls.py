from django.urls import path 
from parkly import views


urlpatterns = [
    path('' , views.home , name= "home" ),
    path('owner/register' , views.registerParking , name= "registerParking" ),
    
]