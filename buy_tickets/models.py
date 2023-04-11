from django.db import models
from django.contrib.auth.models import User


class BusTrip(models.Model):
    depart_city = models.CharField(
        max_length=100,
        verbose_name='Departure City',
        help_text='Enter a departure city name'
    )

    arrival_city = models.CharField(
        max_length=100,
        verbose_name='Arrival City',
        help_text='Enter an arrival city name'
    )

    departure_time = models.TimeField(
        help_text='Enter departure time')

    arrival_time = models.TimeField(
        help_text='Enter arrival time',
    )
    price = models.IntegerField(
        verbose_name='Price',
        help_text='Enter the price'
    )

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return '%s %s %s' % (self.depart_city, '-', self.arrival_city)


class Day(models.Model):
    trip = models.ForeignKey(BusTrip, on_delete=models.CASCADE, verbose_name='Your trip')
    date = models.DateField(verbose_name='Date of trip')
    available_seats = models.PositiveIntegerField()


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.CharField(max_length=100)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    passenger_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    price = models.IntegerField()
    number_of_seats = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField(null=False)

    def __str__(self):
        return '%s, %s, %s' % (self.departure_date, self.trip, self.number_of_seats)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=False)
    orders = models.ForeignKey(Ticket, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return '%s' % self.phone_number
