from django import forms
from .models import Reservation, Customer, StartTime, MatchDuration, Court
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
        fields = ('court','date','start_time','duration')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_time'].queryset = StartTime.objects.all()
        self.fields['duration'].queryset = MatchDuration.objects.all()
        self.fields['court'].queryset = Court.objects.all()
        self.fields['start_time'].widget.attrs['class'] = 'form-control'
        self.fields['duration'].widget.attrs['class'] = 'form-control'
        self.fields['court'].widget.attrs['class'] = 'form-control'
        self.fields['date'].widget = DatePicker(options={'minDate': today.strftime('%m-%d-%Y'),'maxDate': max_date.strftime('%m-%d-%Y')})
        self.fields['date'].widget.attrs['class'] = 'form-control'

