from django.shortcuts import render, redirect
from website.models import Reservation, Customer, Court, StartTime, MatchDuration
import pandas as pd
from datetime import date as dt, datetime, time, timedelta
from django.db.models import Q
from . import forms
from django.views.generic import CreateView


def index(request):
    return render(request, 'index.html', {})


def reservations(request):
    # Si no esta logueado lo redireccionamos al login
    if request.user.is_authenticated == False:
        return render(request, "index.html", {'message':'Debe loguearse primero'})

    # Ahora verificamos si hizo una consulta
    form = forms.ReservationForm()
    
    if request.method == "GET":
        context = {'reservations':create_filled_context(request), 'form':form, 'current_date':get_date(request)} 
        return render(request, "reservations.html",context)
    elif request.method == "POST" and 'filtrar' in request.POST:
        context = {'reservations':create_filled_context(request), 'form':form, 'current_date':get_date(request)}
        return render(request, "reservations.html", context)
    elif request.method == "POST" and 'reservar' in request.POST:
        form = forms.ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            customers = Customer.objects.all()
            customer = customers.get(user=request.user)

            if Reservation.objects.filter(date=form['date'].value(), customer=customer).count() >= 3:
                message = "No se permiten más de 3 reservas al día por cliente."
                return render(request, "reservations.html", {'reservations':create_filled_context(request), 
                                                            'form':forms.ReservationForm, 'current_date':get_date(request),
                                                            'message':message})
            reservation.customer = customer
            reservation.save()
            context = {'reservations':create_filled_context(request), 'form':forms.ReservationForm, 'current_date':get_date(request)} 
            return render(request, "reservations.html",context)
        context = {'reservations':create_filled_context(request), 'form':forms.ReservationForm, 'current_date':get_date(request)} 
        return render(request, "reservations.html",context)

    else:
        context = {'reservations':create_filled_context(request), 'form':forms.ReservationForm, 'current_date':get_date(request)} 
        return render(request, "reservations.html",context)


def contact(request):
    return render(request, 'contact.html', {})


class BookView(CreateView):
    form_class = forms.ReservationForm
    template_name = 'book.html'

    def form_valid(self, form):
        customers = Customer.objects.all()
        customer = customers.get(user=self.request.user)
        form.instance.customer = customer
        form.save()
        return super(BookView, self).form_valid(form)

def create_filled_context(request):

    if 'date_filter' in request.POST and request.POST.get('date_filter') != '':
        date = request.POST.get('date_filter')
        index = ['10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30','14:00',
        '14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00','18:30','19:00',
        '19:30','20:00','20:30','21:00','21:30','22:00']

        df=pd.DataFrame(index=index, columns=['time',1,2,3])
        df['time']=index
        reservations = Reservation.objects.all()
        reservations = reservations.filter(Q(date__day=datetime.strptime(date, '%m/%d/%Y').day) & 
        Q(date__month=datetime.strptime(date, '%m/%d/%Y').month) & 
        Q(date__year=datetime.strptime(date, '%m/%d/%Y').year))

        data = []
        df = df.fillna(' ')
        for reservation in reservations:
            end_time = datetime.combine(dt.today(), reservation.start_time.start_time) + reservation.duration.duration
            df.loc[reservation.start_time.start_time.strftime("%H:%M"):end_time.time().strftime("%H:%M"), reservation.court.court_id] = reservation.customer.first_name + ' ' +reservation.customer.last_name
        for i in range(df.shape[0]):
            row = df.iloc[i]
            data.append(dict(row))
        return data
    elif 'reservar' in request.POST and request.POST.get('date') != '':
        date = request.POST.get('date')
        index = ['10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30','14:00',
        '14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00','18:30','19:00',
        '19:30','20:00','20:30','21:00','21:30','22:00']

        df=pd.DataFrame(index=index, columns=['time',1,2,3])
        df['time']=index
        reservations = Reservation.objects.all()
        reservations = reservations.filter(Q(date__day=datetime.strptime(date, '%Y-%m-%d').day) & 
        Q(date__month=datetime.strptime(date, '%Y-%m-%d').month) & 
        Q(date__year=datetime.strptime(date, '%Y-%m-%d').year))

        data = []
        df = df.fillna(' ')
        for reservation in reservations:
            end_time = datetime.combine(dt.today(), reservation.start_time.start_time) + reservation.duration.duration
            df.loc[reservation.start_time.start_time.strftime("%H:%M"):end_time.time().strftime("%H:%M"), reservation.court.court_id] = reservation.customer.first_name + ' ' +reservation.customer.last_name
        for i in range(df.shape[0]):
            row = df.iloc[i]
            data.append(dict(row))
        return data
    else:
        date = datetime.now()
        index = ['10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30','14:00',
        '14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00','18:30','19:00',
        '19:30','20:00','20:30','21:00','21:30','22:00']

        df=pd.DataFrame(index=index, columns=['time',1,2,3])
        df['time']=index
        reservations = Reservation.objects.all()
        reservations = reservations.filter(Q(date__day=date.day) & 
        Q(date__month=date.month) & 
        Q(date__year=date.year))

        data = []
        df = df.fillna(' ')
        for reservation in reservations:
            end_time = datetime.combine(dt.today(), reservation.start_time.start_time) + reservation.duration.duration
            df.loc[reservation.start_time.start_time.strftime("%H:%M"):end_time.time().strftime("%H:%M"), reservation.court.court_id] = reservation.customer.first_name + ' ' +reservation.customer.last_name
        for i in range(df.shape[0]):
            row = df.iloc[i]
            data.append(dict(row))
        return data


def get_date(request):
    if 'date_filter' in request.POST and request.POST.get('date_filter') != '':
        date = datetime.strptime(request.POST.get('date_filter'), '%m/%d/%Y')
        return str(date.day)+'/'+str(date.month)+'/'+str(date.year)
    elif 'date' in request.POST and request.POST.get('date') != '':
        date = datetime.strptime(request.POST.get('date'), '%Y-%m-%d')
        return str(date.day)+'/'+str(date.month)+'/'+str(date.year)
    else:
        date = datetime.now()
        return str(date.day)+'/'+str(date.month)+'/'+str(date.year)
        

    # AJAX
def load_start_times(request):
    if request.GET.get('id_date') != '' and request.GET.get('id_court') != '':
        court_id = request.GET.get('id_court')
        date = request.GET.get('id_date')
        available_start_times = get_available_start_times(court_id, date)

        return render(request, 'start_time_dropdown_list_options.html', {'start_times': available_start_times})
    
    else:
        return render(request, 'start_time_dropdown_list_options.html', {'start_times': []})

    # AJAX
def load_durations(request):
    if request.GET.get('id_date') != '' and request.GET.get('id_court') != '' and request.GET.get('id_start_time') != '':
        court_id = request.GET.get('id_court')
        date = request.GET.get('id_date')
        start_time_id = int(request.GET.get('id_start_time'))
        available_durations = get_available_durations(court_id, date, start_time_id)

        return render(request, 'durations_dropdown_list_options.html', {'durations': available_durations})
    
    else:
        return render(request, 'durations_dropdown_list_options.html', {'durations': []})

def get_available_start_times(court_id, date):

    form_start_times = Reservation.objects.filter(court_id=court_id, date=date).values('start_time')
    durations = Reservation.objects.filter(court_id=court_id, date=date).values('duration')
    available_start_times = StartTime.objects.exclude(start_time_id__in=form_start_times).only('start_time')
    
    zipped = list(zip(form_start_times, durations))

    for start, duration in zipped:
        if duration.get('duration') == 1:
            available_start_times = available_start_times.exclude(start_time_id=start.get('start_time')+1)

        if duration.get('duration') == 2:
            available_start_times = available_start_times.exclude(start_time_id=start.get('start_time')+1)
            available_start_times = available_start_times.exclude(start_time_id=start.get('start_time')+2)
            
        if duration.get('duration') == 3:
            available_start_times = available_start_times.exclude(start_time_id=start.get('start_time')+1)
            available_start_times = available_start_times.exclude(start_time_id=start.get('start_time')+2)
            available_start_times = available_start_times.exclude(start_time_id=start.get('start_time')+3)

    return available_start_times

def get_available_durations(court_id, date, start_time_id):

    durations = MatchDuration.objects.all()
    available_start_times = get_available_start_times(court_id, date)

    if available_start_times.filter(start_time_id=start_time_id+3).exists() and available_start_times.filter(start_time_id=start_time_id+2).exists()\
        and available_start_times.filter(start_time_id=start_time_id+1).exists():
        return durations

    elif available_start_times.filter(start_time_id=start_time_id+2).exists() and available_start_times.filter(start_time_id=start_time_id+1).exists():
        durations = durations.exclude(duration_id=3)

    elif available_start_times.filter(start_time_id=start_time_id+1).exists():
        durations = durations.exclude(duration_id=3)
        durations = durations.exclude(duration_id=2)

    else:
        durations = MatchDuration.objects.none()
    return durations
