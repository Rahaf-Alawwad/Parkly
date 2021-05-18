from django.shortcuts import render
from django.conf import settings
from django.views.generic.base import TemplateView
import stripe
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY
# payments/views.py

class HomePageView(TemplateView):
    template_name = 'subscribe.html'


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
        return render(request, 'charge.html')

# subsrcibe page, temp
def subscribe(request):
    return render(request,'subscribe.html' , {})                 

       