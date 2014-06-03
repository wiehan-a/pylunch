from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from specials.models import Restaurant

def index(request):
    restaurant_list = Restaurant.objects.all().order_by('name')
    context = {'restaurant_list': restaurant_list}
    return render(request, 'specials/restaurant_listing.html', context)

def restaurant_info(request, r_id):
    restaurant = get_object_or_404(Restaurant, pk=r_id)
    context = {'restaurant' : restaurant}
    return render(request, 'specials/restaurant_info.html', context)