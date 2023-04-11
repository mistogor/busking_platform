"""busking_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path as url
from buy_tickets.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('about_us', about_us, name='about_us'),
    path('instructions', instructions, name='instructions'),
    path('get_tickets/', get_tickets, name='get_tickets'),
    path('bustrip_list/', product_list, name='bustrip_list'),
    path('create_days/', create_days, name='create_days'),
    url(r'^register/$', register, name='register'),
    path('profile/<str:username>/orders/', profile_tickets, name='profile_tickets'),
    path('profile/<str:username>/orders/ticket_<int:id>/', profile_ticket_details, name='profile_ticket_details'),
    path('profile/<str:username>/edit/', profile_edit, name='profile_edit'),
    url(r'^login/$', auth, name='login'),
    url(r'^logout/$', log_out, name='logout'),
    url(r'^book_ticket/buy/(?P<id>\d+)$', book_ticket, name= 'book_ticket'),
    url(r'^book_ticket/confirm/(?P<id>\d+)$', confirm_order, name= 'confirm_order'),
]
