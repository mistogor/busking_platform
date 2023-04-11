# Generated by Django 4.1.3 on 2023-01-13 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buy_tickets', '0003_remove_ticket_available_seats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bustrip',
            name='arrival_city',
            field=models.CharField(help_text='Enter an arrival city name', max_length=100, verbose_name='Arrival City'),
        ),
        migrations.AlterField(
            model_name='bustrip',
            name='depart_city',
            field=models.CharField(help_text='Enter a departure city name', max_length=100, verbose_name='Departure City'),
        ),
    ]
