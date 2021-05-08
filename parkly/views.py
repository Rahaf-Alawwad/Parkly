from django.shortcuts import render

# Create your views here.

def home(request):
 
    return  render(request,'home.html' , {}) 



def registerParking(request):
 
    return  render(request,'register_lot.html' , {}) 
