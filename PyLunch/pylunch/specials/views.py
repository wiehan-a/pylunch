from django.shortcuts import render
from django.http import HttpResponse
from specials.models import Restaurant

def index(request):
    restaurant_list = Restaurant.objects.all().order_by('name')
    context = {'restaurant_list': restaurant_list}
    return render(request, 'specials/restaurant_listing.html', context)

def restaurant_info(request, r_id):
    return HttpResponse("Hello, world %s" % r_id)