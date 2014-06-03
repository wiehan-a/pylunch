from django.conf.urls import patterns, url
from specials import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^restaurant/(?P<r_id>\d+)/', views.restaurant_info, name='r_info'),
)