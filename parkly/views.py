from django.shortcuts import render
from datetime import datetime
from .models import Reservation, Parking,Lot
from django.db.models import Q
# Create your views here.

def home(request):
    return  render(request,'home.html' , {}) 




def registerParking(request):
 
    return render(request,'register_lot.html' , {}) 



def reserveParking(request):
    ##Begin##
    #print("request Post: ",request.POST)
    if (request.method == "POST"): 
        available_parkings =[]
        lot = Lot.objects.get(name="King Saud University")
        lot_parkings = Parking.objects.filter(lot=lot) 
        for parking in lot_parkings:
            if Reservation.objects.filter(Q(parking=parking, date=request.POST.get("date"),timeFrom__gte= request.POST.get("timeFrom"),timeTo__lte=request.POST.get("timeTo"))).exists(): 
                available_parkings.append(1)
            else:
                available_parkings.append(0)
        ##End##
        print("available_parkings: ",available_parkings)
        return render(request,'reserve.html' , {"available_parkings":available_parkings, "lot_parkings":lot_parkings}) 
    else:
        return render(request,'reserve.html' , {})
