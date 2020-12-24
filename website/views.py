from django.shortcuts import render, redirect
from website.models import Reservation, Customer, Court
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
        context = {'reservations':create_empty_context(request), 'form':form} 
        return render(request, "reservations.html",context)
    elif request.method == "POST" and 'filtrar' in request.POST:
        context = {'reservations':create_filled_context(request), 'form':form}
        return render(request, "reservations.html", context)
    elif request.method == "POST" and 'reservar' in request.POST:
        form = forms.ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            customers = Customer.objects.all()
            customer = customers.get(user=request.user)
            reservation.customer = customer
            reservation.save()
            context = {'reservations':create_empty_context(request), 'form':forms.ReservationForm} 
            return render(request, "reservations.html",context)
        print(form.errors)
        context = {'reservations':create_empty_context(request), 'form':forms.ReservationForm} 
        return render(request, "reservations.html",context)

    else:
        context = {'reservations':create_empty_context(request), 'form':forms.ReservationForm} 
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
    

def create_empty_context(request):
    index = ['10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30','14:00',
    '14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00','18:30','19:00',
    '19:30','20:00','20:30','21:00','21:30','22:00']

    df=pd.DataFrame(index=index, columns=['time',1,2,3])
    df['time']=index
    df = df.fillna(' ')
    data = []
    for i in range(df.shape[0]):
        row = df.iloc[i]
        data.append(dict(row))
    return data



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
    else:
        return create_empty_context(request)
