from django.urls import path 
from parkly import views
from user import views as user_views

urlpatterns = [
    path('' , views.home , name= "home" ),
    path('lot/add' , views.addLot , name= "addLot" ),
    path('lot/register' , views.registerLot , name= "registerLot" ),
    path('parking/' , views.parkings , name= "parkings" ),
    path('parking/map' , views.parkingMap , name= "parkingMap" ),
    path('parking/available' , views.showParking , name= "showParking" ),
    path('parking/reserve/' , views.reserveParking , name= "reserveParking" ),
    path('profile' , views.profile , name= "profile" ),
    path('search/' , views.search , name= "search" ),
    path('requestSite/' , views.requestSite , name= "requestSite" ),
]