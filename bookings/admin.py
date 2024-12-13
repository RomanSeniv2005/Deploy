from django.contrib import admin
from .models import Route, Ticket, Payment

admin.site.register(Route)
admin.site.register(Ticket)
admin.site.register(Payment)
