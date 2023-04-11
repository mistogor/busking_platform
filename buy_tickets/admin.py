import calendar

from django.contrib import admin
from .models import *
import datetime

admin.site.register(BusTrip)
admin.site.register(Ticket)
admin.site.register(Profile)


def set_available_seats(modeladmin, request, queryset):
    trip = BusTrip.objects.get(pk=1)
    year = 2023

    for month in range(1, 13):
        num_days = calendar.monthrange(year, month)[1]

        for day in range(1, num_days + 1):
            date = datetime.date(year, month, day)
            day, created = Day.objects.get_or_create(trip=trip, date=date)
            day.available_seats = 10
            day.save()


class DayAdmin(admin.ModelAdmin):
    list_display = ['trip', 'date', 'available_seats']
    actions = [set_available_seats]


admin.site.register(Day, DayAdmin)
