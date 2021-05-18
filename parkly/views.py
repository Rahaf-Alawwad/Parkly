from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from .models import *
from user.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .filters import LotFilter
from .forms import RequestForm,RegisterBusinessForm,mapForm
from django.http import HttpResponse
import json
import random 
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .utils import get_geo, get_coordinates,get_zoom
import folium
# Create your views here.
import qrcode
import qrcode.image.svg
from io import BytesIO


def index(request):
    context = {}
    if request.method == "POST":
        factory = qrcode.image.svg.SvgImage
        img = qrcode.make(request.POST.get("qr_text",""), image_factory=factory, box_size=20)
        stream = BytesIO()
        img.save(stream)
        context["svg"] = stream.getvalue().decode()

    return render(request, "qr.html", context=context)

def home(request):
    return render(request,'home.html' , {}) 


def parkingMap(request):
    distance=0
    minutes=0
    mapData=get_object_or_404(Measurement,id=1)
    form = mapForm(request.POST or None)
    geolocate = Nominatim(user_agent='measurements')
    ip="72.14.207.99"
    country, city, lat,long= get_geo(ip)
    location=geolocate.geocode(city)
    print(location)
    locationLatitude = lat
    locationLongitude= long
    fromPoint=(locationLatitude,locationLongitude)
    mapImage= folium.Map(width=500, height=500, location=get_coordinates(locationLatitude,locationLongitude))
    folium.Marker([locationLatitude,locationLongitude], tooltip='Click here for more', popup=city['city'], icon=folium.Icon(color="red")).add_to(mapImage)
    if form.is_valid():
        instance =form.save(commit=False)
        destination_ = form.cleaned_data.get('destination')
        destination = geolocate.geocode(destination_)

        destinationLatitude=destination.latitude
        destinationLongitude=destination.longitude
        toPoint=(destinationLatitude,destinationLongitude)
        distance= round(geodesic(fromPoint,toPoint).km, 2)
        mapImage= folium.Map(width=500, height=500, location=get_coordinates(locationLatitude,locationLongitude,destinationLatitude,destinationLongitude), zoom_start=get_zoom(distance))
        folium.Marker([locationLatitude,locationLongitude], tooltip='Click here for more', popup=city['city'], icon=folium.Icon(color="red")).add_to(mapImage)
        folium.Marker([destinationLatitude,destinationLongitude], tooltip='Click here for more', popup=destination, icon=folium.Icon(color="blue", icon="cloud")).add_to(mapImage)

        connector_line= folium.PolyLine(locations=[fromPoint,toPoint], weight=2, color='black')
        mapImage.add_child(connector_line)
        instance.location = location
        instance.distance = distance
        instance.save()
    mapImage = mapImage._repr_html_()   
    minutes = round(distance/0.6)
    context ={
        'distance': distance,
        'minutes':minutes,
        'form':form,
        'mapImage':mapImage
    }

    return render(request,'map.html',context)


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
   
    form = RegisterBusinessForm(request.POST or None)
    context={
        "form":form
    }
    if (request.method == "POST"):
        owner = Lot.objects.get(pk=request.user.id)
        if (form.is_valid()):
            lot= Lot(form,  owner = owner )
            lot.save()
            return render (request, 'thanks.html')
        else:
            print(form.errors)
    else:
        return render (request, 'owner/register_business.html',context)

 


@login_required
def parkings(request):
   
    lot = Lot.objects.get(pk=request.POST.get("pk"))
    return render(request,'reserve.html' , {"reentery":"No","prices":"0","lot":lot,"date":"","timeFrom":"","timeTo":"","zipped":[]})


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
        print(request.POST.get("lot"))
        lot = Lot.objects.get(pk=request.POST.get("lot"))
        print(lot)
        parkings = Parking.objects.filter(lot=lot) 
        for i ,parking in enumerate(parkings):
            if Reservation.objects.filter(Q(parking=parking, date=date,timeFrom__gte=timeFrom ,timeTo__lte=timeTo) |Q(parking=parking, date=date,timeFrom__lte=timeFrom ,timeTo__gte=timeTo) ).exists(): 
                available_parkings.append(1)
                
            else:
                available_parkings.append(0)
                prices.append(parkings[i].price)
            lot_parkings.append(parkings[i].park_ID)
        ##End##
        zipped = zip(available_parkings,lot_parkings)
        reentery =  "Yes" if parkings[0].is_reentry_allowed else "No"
        return render(request,'reserve.html' , {"reentery":reentery,"prices":prices,"lot":lot,"date":date,"timeFrom":timeFrom,"timeTo":timeTo,"zipped":zipped}) 
    else:
        return render(request,'reserve.html' , {"reentery":"No","prices":"0","lot":"","date":"","timeFrom":"","timeTo":"","zipped":[]})

@login_required()
def reserveParking(request):
    lot = Lot.objects.get(pk=request.POST.get("lot"))
    parking = Parking.objects.get(lot=lot, park_ID=request.POST.get("checked-parking"))
    data = Reservation( user = request.user, date=request.POST.get("date"), timeFrom=request.POST.get("timeFrom"),timeTo=request.POST.get("timeTo") ,parking=parking, cost=float(request.POST.get("price")),code=random. random() )
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