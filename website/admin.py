from django.contrib import admin
from .models import Customer, Reservation, Court

admin.site.register(Customer)
admin.site.register(Court)
admin.site.register(Reservation)
