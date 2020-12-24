from django.contrib import admin
from .models import Customer, Reservation, Court, StartTime, MatchDuration

admin.site.register(Customer)
admin.site.register(Court)
admin.site.register(Reservation)
admin.site.register(StartTime)
admin.site.register(MatchDuration)
