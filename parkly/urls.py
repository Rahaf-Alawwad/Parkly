from django.urls import path 
from parkly import views


urlpatterns = [
    path('' , views.home , name= "home" ),
    path('lot/register' , views.registerParking , name= "registerParking" ),
    path('reserve/' , views.reserveParking , name= "reserveParking" ),
    path('profile/<pk>' , views.profile , name= "profile" ),
    
]