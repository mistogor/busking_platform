# Generated by Django 4.1.3 on 2023-01-12 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buy_tickets', '0002_alter_day_available_seats_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='available_seats',
        ),
    ]
