from django.urls import path 
from parkly import views
from user import views as user_views

urlpatterns = [
    path('' , views.home , name= "home" ),
    path('lot/register' , views.registerParking , name= "registerParking" ),
    path('reserve/' , views.reserveParking , name= "reserveParking" ),
<<<<<<< HEAD
    path('profile/<pk>' , views.profile , name= "profile" ),  
=======
    path('profile/<pk>' , user_views.User , name= "profile" ),
    path('search/' , views.search , name= "search" ),
    path('requestSite/' , views.requestSite , name= "requestSite" ),
    
>>>>>>> 0496177cebceca8e2f6d2f86d750c4f83800a38e
]