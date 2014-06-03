from django.db import models
from geoposition.fields import GeopositionField

MAX_PRICE_FORMAT = 	{
                        'max_digits': 5, 
                        'decimal_places': 2
                    }

MAX_RESTAURANT_NAME_LENGTH = 50
MAX_TELEPHONE_LENGTH = 20

class Restaurant(models.Model):
    name = models.CharField(max_length=MAX_RESTAURANT_NAME_LENGTH, unique=True)
    description = models.TextField()
    phone_number =  models.CharField(max_length=MAX_TELEPHONE_LENGTH, blank=True)
    location = GeopositionField(blank=True)
    address = models.TextField(blank=True)
    url = models.URLField(blank=True)

    def __unicode__(self):
	   return self.name

class Special(models.Model):

    LUNCH = 'LU'
    BREAKFAST = 'BR'
    DINNER = 'DI'
    SPECIAL_TYPES = (
                        (LUNCH, 'Lunch'),
                        (BREAKFAST, 'Breakfast'),
                        (DINNER, 'Dinner'),
                    )

    restaurant = models.ForeignKey(Restaurant)
    description = models.CharField(max_length=MAX_DESCRIPTION_LENGTH)

    special_type = models.CharField(max_length=2, choices=SPECIAL_TYPES)

    special_price = models.DecimalField(**MAX_PRICE_FORMAT)
    normal_price = models.DecimalField(**MAX_PRICE_FORMAT)

    weekdays_valid = models.ManyToManyField(Weekday)
    valid_from = models.DateField(blank=True)
    valid_until = models.DateField(blank=True)

    def __unicode__(self):
	   return "%s: %s" % (self.restaurant.name, self.description)

class Weekday(models.Model):

    DAYS_OF_WEEK = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )

    weekday = models.CharField(max_length=1, choices=DAYS_OF_WEEK, 
                                unique=True, primary_key=True)