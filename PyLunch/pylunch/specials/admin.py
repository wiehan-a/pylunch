from django.contrib import admin
from specials.models import Restaurant, Special, OpenClosedTime

class OpenClosedTimeInline(admin.StackedInline):
    model = OpenClosedTime

class RestaurantAdmin(admin.ModelAdmin):
    inlines = [
        OpenClosedTimeInline
    ]

class SpecialAdmin(admin.ModelAdmin):
    pass

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Special, SpecialAdmin)