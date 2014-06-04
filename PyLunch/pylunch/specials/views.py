from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from specials.models import Restaurant, Special

def index(request):
    context = {}
    Restaurant.add_listing_context(context)
    Special.add_current_special_context(context)
    return render(request, 'specials/restaurant_listing.html', context)

def restaurant_info(request, r_id):
    restaurant = get_object_or_404(Restaurant, pk=r_id)
    context = {'restaurant' : restaurant}
    return render(request, 'specials/restaurant_info.html', context)