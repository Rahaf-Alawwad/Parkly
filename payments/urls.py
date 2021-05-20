# payments/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.subscribe , name= "subscribe"),
    path('subscribe/' , views.subscribe , name= "subscribe" ),
    path('charge/', views.charge, name='charge'),
    path('payment/', views.HomePageView.as_view(), name='payment'),
]