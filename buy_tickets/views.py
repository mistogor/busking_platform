from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from .models import *
from .filters import TripFilter
from .forms import *
import datetime
from django.contrib.auth.decorators import login_required


def index(request):
    today = datetime.date.today()
    f = TripFilter(request.GET, queryset=Day.objects.all())
    return render(request, 'buy_tickets/index.html', {'filter': f})

def about_us(request):
    return render(request, 'buy_tickets/about_us.html')

def instructions(request):
    return render(request, 'buy_tickets/instructions.html')
    
    
def product_list(request):
    today = datetime.date.today()
    f = TripFilter(request.GET, queryset=Day.objects.all())

    return render(request, 'buy_tickets/tickets.html', {'filter': f})


@login_required
def book_ticket(request, id):
    user = request.user

    profile = Profile.objects.get(user=user)
    day = Day.objects.get(id=id)

    phone_number = profile.phone_number
    departure_time = day.trip.departure_time
    arrival_time = day.trip.arrival_time
    passenger_name = user.first_name + ' ' + user.last_name

    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            departure_date = form.cleaned_data['departure_date'] #возможно заменить на day.date???
            if departure_date < datetime.date.today():
                messages.error(request, 'You can`t bus tickets in past! Please choose correct date.')
                return render(request, 'buy_tickets/own_tickets.html', {'form': form,
                                                                        'id': id,
                                                                        'phone_number': phone_number,
                                                                        'user': user,
                                                                        'trip': day.trip,
                                                                        'departure_time': day.trip.departure_time,
                                                                        'arrival_time': day.trip.arrival_time,
                                                                        'price': day.trip.price
                                                                        })
            else:
                day = Day.objects.get(trip=day.trip, date=departure_date)
                number_of_seats = form.cleaned_data['number_of_seats']
                if number_of_seats <= day.available_seats != 0:
                    price = form.cleaned_data['price']
                    seats = day.available_seats
                    total_price = int(number_of_seats) * int(price)
                    available_seats = int(seats) - int(number_of_seats)
                    day.available_seats = available_seats
                    day.save()
                    form.price = total_price
                    form.total_price = total_price
                    ticket = form.save()
                    ticket.total_price = total_price
                    ticket.save()
                    messages.success(request, 'Your order is saved to your profile!')
                    return redirect('confirm_order', id=ticket.id)
                else:
                    messages.error(request, f"We don`t have so much available seats. There`s {day.available_seats} "
                                            f"seats. "
                                            f"Please try again or choose another date.")
                    return render(request, 'buy_tickets/own_tickets.html', {'form': form,
                                                                            'id': id,
                                                                            'phone_number': phone_number,
                                                                            'user': user,
                                                                            'trip': day.trip,
                                                                            'departure_time': day.trip.departure_time,
                                                                            'arrival_time': day.trip.arrival_time,
                                                                            'price': day.trip.price
                                                                            })
        else:
            messages.error(request, 'Form is invalid')
            return render(request, 'buy_tickets/own_tickets.html', {'form': form,
                                                                    'id': id,
                                                                    'phone_number': phone_number,
                                                                    'user': user,
                                                                    'trip': day.trip,
                                                                    'departure_time': day.trip.departure_time,
                                                                    'arrival_time': day.trip.arrival_time,
                                                                    'price': day.trip.price
                                                                    })
    else:
        form = TicketForm(initial={
            'trip': day.trip,
            'user': user,
            'departure_time': day.trip.departure_time,
            'arrival_time': day.trip.arrival_time,
            'passenger_name': passenger_name,
            'phone_number': phone_number,
            'number_of_seats': '1',
            'total_price': day.trip.price,
            'price': int(day.trip.price) * int('1')

        })
        return render(request, 'buy_tickets/own_tickets.html', {
            'form': form,
            'id': id,
            'phone_number': phone_number,
            'user': user,
            'trip': day.trip,
            'departure_time': day.trip.departure_time,
            'arrival_time': day.trip.arrival_time,
            'total_price': day.trip.price,
            'price': day.trip.price
        })


@login_required
def confirm_order(request, id):
    order = Ticket.objects.get(id=id)
    return render(request, 'buy_tickets/own_success.html', {'order': order})


def get_tickets(request, id):
    depart_city = BusTrip.depart_city.all()
    arrival_city = BusTrip.arrival_city.all()
    departure_time = BusTrip.departure_time.all()
    arrival_time = BusTrip.arrival_time.all()
    price = BusTrip.price.all()
    myFilter = TripFilter(request.GET, queryset=depart_city)
    context = {
        'depart_city': depart_city,
        'arrival_city': arrival_city,
        'departure_time': departure_time,
        'arrival_time': arrival_time,
        'price': price,
        'myFilter': myFilter,
    }

    return render(request, 'buy_tickets/tickets.html',
                  context=context)


def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return render(request, 'buy_tickets/register_done.html')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'buy_tickets/register.html', {'user_form': user_form, 'profile_form': profile_form})


def auth(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! ')
            return redirect('/bustrip_list')
        else:
            messages.info(request, 'Something went wrong. Please try again!')
            return redirect('/login')
    else:
        return render(request, 'buy_tickets/login.html')


@login_required
def profile_tickets(request, username):
    user = User.objects.get(username=username)
    orders = Ticket.objects.filter(user=user)
    return render(request, 'buy_tickets/profile_tickets.html', {'orders': orders, 'username': user.username})

@login_required
def profile_ticket_details(request, username, id):
    user = User.objects.get(username=username)
    order = Ticket.objects.get(id=id)
    return render(request, 'buy_tickets/profile_ticket_details.html', {'order': order, 'username': user.username})


@login_required
def profile_edit(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        user_edit_form = UserEditForm(request.POST, instance=user)
        profile_edit_form = ProfileEditForm(request.POST, instance=profile)
        if user_edit_form.is_valid() and profile_edit_form.is_valid():
            user_edit_form.save()
            profile_edit_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile_edit', username=user.username)
    else:
        user_edit_form = UserEditForm(instance=user)
        profile_edit_form = ProfileEditForm(instance=profile)
    context = {
        'user_edit_form': user_edit_form,
        'profile_edit_form': profile_edit_form,
    }
    return render(request, 'buy_tickets/profile_edit.html', context)


@login_required
def log_out(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")


def create_days(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = CreateDaysForm(request.POST)
            if form.is_valid():
                trip = form.cleaned_data['trip']
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                available_seats = form.cleaned_data['available_seats']
                current_date = start_date
                while current_date <= end_date:
                    if not Day.objects.filter(trip=trip, date=current_date).exists():
                        Day.objects.create(
                            trip=trip,
                            date=current_date,
                            available_seats=available_seats
                        )
                        current_date += datetime.timedelta(days=1)
                    else:
                        current_date += datetime.timedelta(days=1)

                messages.success(request, 'Days were created')
                return render(request, 'buy_tickets/create_days.html', {'form': form})

        else:
            form = CreateDaysForm()
            return render(request, 'buy_tickets/create_days.html', {'form': form})

    else:
        return HttpResponseNotFound("You have no rights to watch this page!")
