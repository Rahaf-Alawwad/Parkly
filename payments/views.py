from django.shortcuts import render
from django.conf import settings
from django.views.generic.base import TemplateView
import stripe
from parkly.models import *
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY
# payments/views.py

class HomePageView(TemplateView):
    template_name = 'payment.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

def charge(request):
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=500,
            currency='usd',
            description='A Parkly charge',
            source=request.POST['stripeToken'],
        )

        lot = Lot.objects.get(pk=request.POST.get("lot"))
        parking = Parking.objects.get(lot=lot, park_ID=request.POST.get("checked-parking"))
        data = Reservation( user = request.user, date=request.POST.get("date"), timeFrom=request.POST.get("timeFrom"),timeTo=request.POST.get("timeTo") ,parking=parking, cost=float(request.POST.get("price")),code=random. random() )
        data.save()
        return render(request, 'charge.html')

# subsrcibe page, temp
def subscribe(request):
    return render(request,'subscribe.html' , {})                 

       