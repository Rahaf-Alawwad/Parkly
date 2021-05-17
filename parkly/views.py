from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from .models import *
from user.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .filters import LotFilter
from .forms import RequestForm,RegisterBusinessForm
from django.http import HttpResponse
import json

# Create your views here.

def home(request):
    return render(request,'home.html' , {}) 

@login_required()
def profile(request):
 
    context = {}
    user = request.user
   
    if user.is_authenticated:
        context['profile'] = get_object_or_404(User, username=user)
        return render(request, 'profile.html', context)
    return redirect('login')     


@login_required()
def addLot(request):
 
    return render(request,'add_lot.html' , {}) 

@login_required()
def registerLot(request):

    if (request.method == "POST"):
        lot = RegisterBusinessForm(request.POST or None)
        if (lot.is_valid()):
            lot.save()
            return render (request, 'thanks.html')
        else:
            print(lot.errors)
    else:
        return render (request, 'owner/register_business.html')

 
    


@login_required
def parkings(request):
   
    lot = Lot.objects.get(pk=request.POST.get("pk"))
    return render(request,'reserve.html' , {"prices":"-","lot":lot,"date":"","timeFrom":"","timeTo":"","zipped":[]})


@login_required()
def showParking(request):
    
    ##Begin##
    #print("request Post: ",request.POST)
    if (request.method == "POST"): 
        available_parkings =[]
        lot_parkings=[]
        prices=[]
        date=request.POST.get("date")
        timeFrom=request.POST.get("timeFrom")
        timeTo=request.POST.get("timeTo")
        lot = Lot.objects.get(pk=request.POST.get("lot"))
        print(lot)
        parkings = Parking.objects.filter(lot=lot) 
        for i ,parking in enumerate(parkings):
            if Reservation.objects.filter(Q(parking=parking, date=date,timeFrom__gte=timeFrom ,timeTo__lte=timeTo)).exists(): 
                available_parkings.append(1)
                
            else:
                available_parkings.append(0)
                prices.append(parkings[i].price)
            lot_parkings.append(parkings[i].park_ID)
        ##End##
        zipped = zip(available_parkings,lot_parkings)
        return render(request,'reserve.html' , {"prices":prices,"lot":lot,"date":date,"timeFrom":timeFrom,"timeTo":timeTo,"zipped":zipped}) 
    else:
        return render(request,'reserve.html' , {"prices":"-","lot":"","date":"","timeFrom":"","timeTo":"","zipped":[]})


def reserveParking(request):
    lot = Lot.objects.get(pk=request.POST.get("lot"))
    parking = Parking.objects.get(lot=lot, park_ID=request.POST.get("checked-parking"))
    data = Reservation( user = request.user, date=request.POST.get("date"), timeFrom=request.POST.get("timeFrom"),timeTo=request.POST.get("timeTo") ,parking=parking, cost=float(request.POST.get("price")),code="10341")
    data.save()
    return render(request,'thanks.html' , {})

@login_required()
def search(request):
    search =request.POST.get("search")
    lotsFilter=[]
    lots=Lot.objects.all()
    filter= LotFilter(request.GET, queryset=lots)
    if (request.method == "POST"): 
        lotSearch = Lot.objects.filter(Q(name__icontains=search) | Q(location__icontains=search))
        for lot in lotSearch:
            lotsFilter.append(lot)
    else:
        lotsFilter=filter.qs
    length =(len(lotsFilter))
    context={"filter":filter,"lotsFilter":lotsFilter, "search":search, "length":length}
    return render (request, 'search.html',context)

@login_required()
def requestSite(request):
   
    if (request.method == "POST"):
        site = RequestForm(request.POST or None)
        if (site.is_valid()):
            site.save()
            return render (request, 'thanks.html')
        else:
            print(site.errors)
    else:
        return render (request, 'site_request.html')



