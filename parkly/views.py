from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from .models import *
from user.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .filters import LotFilter
from .forms import RequestForm,RegisterBusinessForm,mapForm
from django.contrib import messages
import random 
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .utils import get_geo, get_coordinates,get_zoom
import folium
# Create your views here.
import qrcode
import qrcode.image.svg
from io import BytesIO
from django.db.models import Count





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
    ip="2.89.237.20" #request.META.get("REMOTE_ADDR")
    country, city, lat,long= get_geo(ip)
    location=geolocate.geocode(city)
    locationLatitude = lat
    locationLongitude= long
    fromPoint=(locationLatitude,locationLongitude)
    mapImage= folium.Map(width=500, height=500, location=get_coordinates(locationLatitude,locationLongitude))
    folium.Marker([locationLatitude,locationLongitude], tooltip='Click here for more', popup=city['city'], icon=folium.Icon(color="red", icon="user")).add_to(mapImage)
    if form.is_valid():
        instance =form.save(commit=False)
        destination_ = form.cleaned_data.get('destination')
        destination = geolocate.geocode(destination_)

        destinationLatitude=destination.latitude
        destinationLongitude=destination.longitude
        toPoint=(destinationLatitude,destinationLongitude)
        distance= round(geodesic(fromPoint,toPoint).km, 2)
        mapImage= folium.Map(width=500, height=500, location=get_coordinates(locationLatitude,locationLongitude,destinationLatitude,destinationLongitude), zoom_start=get_zoom(distance))
        folium.Marker([locationLatitude,locationLongitude], tooltip='Click here for more', popup=city['city'], icon=folium.Icon(color="red",icon="user")).add_to(mapImage)
        folium.Marker([destinationLatitude,destinationLongitude], tooltip='Click here for more', popup=destination, icon=folium.Icon(color="blue")).add_to(mapImage)

        connector_line= folium.PolyLine(locations=[fromPoint,toPoint], weight=2, color='green')
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
        all_reservation=Reservation.objects.filter(Q(user=request.user))
        try:
            context['latest']= all_reservation.order_by('date')[0].parking.lot

        except:
            context['latest']="No reservation"

        try:
            context['frequent']=all_reservation.values_list('parking').annotate(lot_count=Count('parking.lot')).order_by('-lot_count')[0]

        except:
            context['frequent']="No reservation"

        return render(request, 'user_profile.html', context)
    return redirect('login')     







@login_required()
def user_edit(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        context['profile'] = get_object_or_404(User, username=user)
        
        if (request.method == "POST"):
            if request.POST.get('img') == "":
                img = user.img
            else:
                img = request.POST.get('img')
            User.objects.filter(pk=request.user.id).update(email=request.POST.get('email'),first_name=request.POST.get('first_name'),last_name=request.POST.get('last_name'),contact_number=request.POST.get('contact_number'),location=request.POST.get('location'),img=img)
            return render(request, 'user_profile.html', context)
        else:
            return render(request, 'user_edit.html', context)
    return redirect('login')   






@login_required()
def user_delete(request):
        user = User.objects.get(pk=request.user.id)
        user.delete()
        messages.success(request, "The account is deleted") 
        return render(request,'home.html' , {})  




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
        
        if (form.is_valid()):
            form = form.save(commit=False)
            lot= Lot(name =form.name,location =form.location,available_parking =form.available_parking,is_reentry_allowed =form.is_reentry_allowed, price=form.price, owner = request.user )
            lot.save()
            request.user.user_type=2
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
                prices.append(lot.price)
            lot_parkings.append(parkings[i].park_ID)
   
        zipped = zip(available_parkings,lot_parkings)
        reentery =  "Yes" if lot.is_reentry_allowed else "No"
        return render(request,'reserve.html' , {"reentery":reentery,"prices":prices,"lot":lot,"date":date,"timeFrom":timeFrom,"timeTo":timeTo,"zipped":zipped}) 
    else:
        return render(request,'reserve.html' , {"reentery":"No","prices":"0","lot":"","date":"","timeFrom":"","timeTo":"","zipped":[]})







@login_required()
def reserveParking(request):
    lot = Lot.objects.get(pk=request.POST.get("lot"))
    parking = Parking.objects.get(lot=lot, park_ID=request.POST.get("checked-parking"))
    data = Reservation(code="https://chart.googleapis.com/chart?cht=qr&chl=" + round(random.random()) + "&chs=160x160&chld=L|0", user = request.user, date=request.POST.get("date"), timeFrom=request.POST.get("timeFrom"),timeTo=request.POST.get("timeTo") ,parking=parking, cost=float(request.POST.get("price")) )
    data.save()
    return render(request,'thanks.html' , {})






@login_required()
def all_reservation(request):
    user=request.user
    allReservations=Q()
    first=True
    if(user.user_type=="2"):
        lot = Lot.objects.get(owner=user)
        allParkings=Parking.objects.filter(lot=lot)
        for parking in allParkings:
            result=Reservation.objects.filter(parking=parking)
          
            if first and len(result)>0 :
                allReservations=result
            
                first=False
            elif len(result)>0:  
                allReservations.union(result)

        
        return render(request,'owner/reservations.html' , {"allReservations":allReservations})
    else:
        return redirect('home')







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





@login_required()
def lot_scanner(request):
    user=request.user
    if(user.user_type=="2"):
        return render (request, 'owner/scanner.html')
    else:
        return render (request, 'home.html')

#paypal checkout
def simpleCheckout(request):
    return render (request, 'simple_checkout.html')

def success(request):
    print('Hi')
    return render (request, 'qr.html')
