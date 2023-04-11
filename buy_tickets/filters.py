import datetime

import django_filters
from .models import Day
from django import forms


class TripFilter(django_filters.FilterSet):
    departure_city = django_filters.CharFilter(field_name='trip__depart_city', lookup_expr='iexact', label='Departure city', widget = forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter departure city', 'required': True
    }))
    arrival_city = django_filters.CharFilter(field_name='trip__arrival_city', lookup_expr='iexact', label='Arrival city', widget = forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter arrival city', 'required': True
    }))
    date = django_filters.DateFilter(label='Departure date',widget = forms.DateInput(
        attrs={'class': 'form-control', 'type': 'date', 'required': True
    }))
    available_seats = django_filters.NumberFilter(lookup_expr='gte', label='Number of seats', widget = forms.NumberInput(
        attrs={'class': 'form-control', 'required': True
    }))

    class Meta:
        model = Day
        fields = ['departure_city', 'arrival_city', 'date', 'available_seats']



