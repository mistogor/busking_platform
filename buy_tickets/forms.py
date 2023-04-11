import datetime

from django import forms
from django.forms import Select, DateInput
import datetime
from django.contrib.auth.models import User

from .models import *


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'
        widgets = {'trip': forms.HiddenInput(),
                   'user': forms.HiddenInput(),
                   'departure_time': forms.HiddenInput(),
                   'arrival_time': forms.HiddenInput(),
                   'total_price': forms.HiddenInput(),
                   'passenger_name': forms.HiddenInput(),
                   'price': forms.HiddenInput(),
                   'departure_date': forms.DateInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Select a date',
                                                            'type': 'date'})
                   }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input your username'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Input your password'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input your last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Input your e-mail'})

        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input your phone number'}),
        }


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input your username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input your last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Input your e-mail'})

        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input your phone number'}),
        }


class CreateDaysForm(forms.ModelForm):
    start_date = forms.DateField(widget= forms.DateInput(attrs={'class': 'form-control',
                                                                'placeholder': 'Input end date',
                                                                'type': 'date'}))
    end_date = forms.DateField(widget= forms.DateInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Input end date',
                                                              'type': 'date'}))

    class Meta:
        model = Day
        fields = ['trip', 'available_seats']
        widgets = {
            'available_seats': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Input number of '
                                                                                                'available seats'}),
            'trip': forms.Select()
        }