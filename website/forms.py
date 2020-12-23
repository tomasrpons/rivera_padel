from django import forms
from .models import Reservation, Customer
from tempus_dominus.widgets import DatePicker
from datetime import datetime as dt
from datetime import timedelta
from django.urls import reverse

today = dt.now()
delta = timedelta(days=7)
max_date = today + delta


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('start_time','duration','court','date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_time'].widget.attrs['class'] = 'form-control'
        self.fields['duration'].widget.attrs['class'] = 'form-control'
        self.fields['court'].widget.attrs['class'] = 'form-control'
        self.fields['date'].widget = DatePicker(options={'format': 'M/D/YYYY','minDate': today.strftime('%m-%d-%Y'),'maxDate': max_date.strftime('%m-%d-%Y')})
        