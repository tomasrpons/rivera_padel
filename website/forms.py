from django import forms
from .models import Reservation, Customer, StartTime, MatchDuration, Court
from datetime import datetime as dt
from datetime import timedelta


today = dt.now()
delta = timedelta(days=14)
max_date = today + delta


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('court','date','start_time','duration')
        widgets = {'date' : forms.DateInput(
            attrs={'type':'date', 'class':'form-control', 'id':'id_reservations_date'}
            
            )}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_time'].queryset = StartTime.objects.all()
        self.fields['duration'].queryset = MatchDuration.objects.all()
        self.fields['court'].queryset = Court.objects.all()

        self.fields['start_time'].widget.attrs['class'] = 'form-control'
        self.fields['duration'].widget.attrs['class'] = 'form-control'
        self.fields['court'].widget.attrs['class'] = 'form-control'


class FilteringForm(forms.Form):
    filtering_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date','class':'form-control','id':'id_filtering_date'}),label="", help_text="")

