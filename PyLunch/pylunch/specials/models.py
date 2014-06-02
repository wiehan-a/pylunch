from django.db import models

MAX_PRICE_FORMAT = 	{
						'max_digits': 5, 
						'decimal_places': 2
				    }

SPECIAL_TYPES = (
					('LU', 'Lunch'),
					('BR', 'Breakfast'),
					('DI', 'Dinner'),
				)

MAX_RESTAURANT_NAME_LENGTH = 50
MAX_DESCRIPTION_LENGTH = 500

class Restaurant(models.Model):
	name = models.CharField(max_length=MAX_RESTAURANT_NAME_LENGTH)
	description = models.CharField(max_length=MAX_DESCRIPTION_LENGTH)

class Special(models.Model):
	restaurant = models.ForeignKey(Restaurant)
	description = models.CharField(max_length=MAX_DESCRIPTION_LENGTH)

	special_type = models.CharField(max_length=2, choices=SPECIAL_TYPES)

	special_price = models.DecimalField(**MAX_PRICE_FORMAT)
	normal_price = models.DecimalField(**MAX_PRICE_FORMAT)