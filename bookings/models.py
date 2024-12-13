from django.db import models
from django.contrib.auth.models import User

class Route(models.Model):
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Ticket(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    status = models.CharField(max_length=10, choices=[('booked', 'Заброньовано'), ('paid', 'Оплачено')])
    first_name = models.CharField(max_length=100, verbose_name="Ім'я", default='Name')
    last_name = models.CharField(max_length=100, verbose_name="Прізвище", default='surname')
    email = models.EmailField(verbose_name="Електронна пошта", default="example@example.com")

class Payment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('completed', 'Completed')])
    payment_date = models.DateTimeField(auto_now_add=True)
