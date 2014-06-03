from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from specials.models import Restaurant

def index(request):
    restaurant_list = Restaurant.objects.all().order_by('name')
    
    first_letters = [(r, r.name[0:1]) for r in restaurant_list]
    length = len(first_letters)
    split = (length+3)/4
    groups = []
    for i in xrange(4):
        groups.append(first_letters[i*split: (i+1)*split])
    for idx in xrange(0, 3):
        while groups[idx][-1][1] == groups[idx+1][0][1]:
            groups[idx+1].insert(0, groups[idx][-1])
            del groups[idx][-1]

    restaurant_groups = [
                            {
                                "start_letter" : group[0][1],
                                "end_letter" : group[-1][1],
                                "restaurant_list" : [r for r, _ in group]
                            }
                            for group in groups
                        ]
    print restaurant_groups

    context = {'restaurant_groups': restaurant_groups}
    return render(request, 'specials/restaurant_listing.html', context)

def restaurant_info(request, r_id):
    restaurant = get_object_or_404(Restaurant, pk=r_id)
    context = {'restaurant' : restaurant}
    return render(request, 'specials/restaurant_info.html', context)