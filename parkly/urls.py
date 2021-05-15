from django.urls import path 
from parkly import views
from user import views as user_views

urlpatterns = [
    path('' , views.home , name= "home" ),
    path('lot/register' , views.registerParking , name= "registerParking" ),
    path('reserve/' , views.reserveParking , name= "reserveParking" ),
    path('profile' , views.profile , name= "profile" ),
    path('search/' , views.search , name= "search" ),
    path('requestSite/' , views.requestSite , name= "requestSite" ),
]