from django.db import models
from geoposition.fields import GeopositionField
from datetime import datetime, time, date

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

    def __unicode__(self):
        return (d for c, d in Weekday.DAYS_OF_WEEK 
                    if int(self.weekday) == c).next()

class Restaurant(models.Model):

    MAX_RESTAURANT_NAME_LENGTH = 50
    MAX_TELEPHONE_LENGTH = 50
    MAX_URL_LENGTH = 200
    MAX_SSID_LENGTH = 64
    MAX_WIFI_PASSWORD_LENGTH = 64


    name = models.CharField(max_length=MAX_RESTAURANT_NAME_LENGTH, unique=True)
    description = models.TextField()
    phone_number =  models.CharField(max_length=MAX_TELEPHONE_LENGTH, blank=True)
    email_address = models.EmailField(blank=True)
    url = models.CharField(max_length=MAX_URL_LENGTH, blank=True)
    has_free_wifi = models.BooleanField(default=False)
    wifi_ssid = models.CharField(max_length=MAX_SSID_LENGTH, blank=True)
    wifi_password = models.CharField(max_length=MAX_WIFI_PASSWORD_LENGTH, blank=True)
    address = models.TextField(blank=True)
    location = GeopositionField(blank=True)
    
    class Meta:
        ordering = ('name',)

    def __unicode__(self):
       return self.name

    @staticmethod
    def add_listing_context(context, num_groups=4):
        """
            Augment context with a list of all restaurants, grouped
            by starting letter. This results in roughly num_groups
            groups of approximately equal size.
        """

        restaurant_list = Restaurant.objects.all().order_by('name')
        
        first_letters = [(r, r.name[0:1]) for r in restaurant_list]
        length = len(first_letters)
        split = (length+num_groups-1)/num_groups
        groups = []
        
        for i in xrange(num_groups):
            groups.append(first_letters[i*split: (i+1)*split])
        for idx in xrange(num_groups-1):
            while groups[idx][-1][1] == groups[idx+1][0][1]:
                groups[idx+1].insert(0, groups[idx][-1])
                del groups[idx][-1]

        restaurant_groups = [
                                {
                                    "start_letter" : group[0][1],
                                    "end_letter" : group[-1][1],
                                    "restaurant_list" : 
                                            [r for r, _ in group]
                                }
                                for group in groups
                            ]

        context['restaurant_groups'] = restaurant_groups

class OpenClosedTime(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    weekday = models.ForeignKey(Weekday)
    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)
    closed_all_day = models.BooleanField(default=False)

    # def __unicode__(self):
    #     return 

class Special(models.Model):

    LUNCH = 'LU'
    BREAKFAST = 'BR'
    DINNER = 'DI'
    ALL_DAY = 'AL'
    SPECIAL_TYPES = (
                        (LUNCH, 'Lunch'),
                        (BREAKFAST, 'Breakfast'),
                        (DINNER, 'Dinner'),
                        (ALL_DAY, 'All day')
                    )

    # Times are in UTC
    SPECIAL_TIMES = {
                        LUNCH : (time(9,0,0), time(15,0,0)),
                        BREAKFAST: (time(6,0,0), time(9,0,0)),
                        DINNER: (time(15,0,0), time(23,59,59)),
                        ALL_DAY: (time(0,0,0), time(23,59,59))
                    }

    MAX_PRICE_FORMAT =  {
                            'max_digits': 5, 
                            'decimal_places': 2
                        }

    restaurant = models.ForeignKey(Restaurant)
    description = models.TextField()

    all_day_flag = models.BooleanField(default=False, blank=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    half_price_flag = models.BooleanField(default=False, blank=True)
    special_price = models.DecimalField(blank=True, null=True, **MAX_PRICE_FORMAT)
    normal_price = models.DecimalField(blank=True, null=True, **MAX_PRICE_FORMAT)

    weekdays_valid = models.ManyToManyField(Weekday)
    valid_permanently = models.BooleanField(default=True)
    valid_from = models.DateField(blank=True, null=True)
    valid_until = models.DateField(blank=True, null=True)

    enabled = models.BooleanField(default=True)
    verified = models.BooleanField(default=True)

    def __unicode__(self):
	   return "%s: %s" % (self.restaurant.name, self.description)

    @staticmethod
    def get_current_special_type(current_time):
        try:
            return (special_type 
                        for special_type, _ in Special.SPECIAL_TYPES
                            if Special.SPECIAL_TIMES[special_type][0] < current_time
                                and Special.SPECIAL_TIMES[special_type][1] > current_time
                    ).next()
        except StopIteration:
            return None

    @staticmethod
    def get_valid_now_queryset():
        """
            Retrieve the specials that are currently valid.
            Returns:
            - time_specific_specials : specials only valid for a window of time
            - all_day_specials : specials that are valid all day
        """

        current_datetime =  datetime.now()
        current_date = current_datetime.date()
        current_time = current_datetime.time()
        current_weekday = current_datetime.weekday()

        valid_queryset = Special.objects.filter(
            (models.Q(valid_from__lte=current_date) & 
                models.Q(valid_until__gte=current_date)) |
            (models.Q(valid_permanently=True))
        ).filter(
            models.Q(verified=True) & models.Q(enabled=True)
        ).filter(
            weekdays_valid__weekday=current_weekday
        )

        time_specific_specials = valid_queryset.filter(
            models.Q(start_time__lte=current_time) &
                models.Q(end_time__gte=current_time)
        )

        all_day_specials = valid_queryset.filter(
            models.Q(all_day_flag=True) | 
                (models.Q(start_time__isnull=True) &
                    models.Q(end_time__isnull=True))
        )

        return time_specific_specials, all_day_specials


    @staticmethod
    def add_current_special_context(context):
        """
            Add to context:
            - "Time of day" specials
            - All day specials
        """
        current_datetime =  datetime.now()
        current_time = current_datetime.time()
        valid_special_type = Special.get_current_special_type(current_time)

        time_specific_specials, all_day_specials = Special.get_valid_now_queryset()

        try:
            context['special_type'] = (y for x, y in Special.SPECIAL_TYPES 
                                        if x==valid_special_type).next()
        except StopIteration:
            pass
        context['time_specific_specials'] = time_specific_specials
        context['all_day_specials'] = all_day_specials


    @staticmethod
    def add_restaurant_specials_context(restaurant, context):
        """
            Add the specials of the current restaurant to the
            context.
        """

        time_specific_specials, all_day_specials = Special.get_valid_now_queryset()
        all_valid = (time_specific_specials | all_day_specials).filter(restaurant=restaurant).all()
        all_specials = Special.objects.filter(restaurant=restaurant).all()
        all_invalid = set(all_specials) - set(all_valid)
        context['valid_specials'] = all_valid
        context['invalid_specials'] = all_invalid





