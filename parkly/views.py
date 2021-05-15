from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from .models import *
from user.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .filters import LotFilter
from .forms import RequestForm
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
def registerParking(request):
 
    return render(request,'register_lot.html' , {}) 


@login_required()
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
        return render(request,'reserve.html' , {"available_parkings":[], "lot_parkings":[]})

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



