from django.db import models
from django.contrib.auth.models import User
import datetime as dt
from django.urls import reverse

time_choices = [ (dt.timedelta(hours=1), '1 hora'), (dt.timedelta(minutes=90), '1 hora y media'), (dt.timedelta(hours=2), '2 horas')]
day_choices = ((0,'Lunes'),(1,'Martes'),(2,'Miercoles'),(3,'Jueves'),(4,'Viernes'),(5,'Sabado'),(6,'Domingo'))


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,blank=False)
    first_name = models.CharField(max_length=50, verbose_name='Nombre')
    last_name = models.CharField(max_length=50, verbose_name='Apellido')
    telephone = models.IntegerField(blank=True,null=True, verbose_name='Telefono')

    def __str__(self):
        return self.first_name


class Court(models.Model):
    court_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,verbose_name='Cancha')

    def __str__(self):
        return self.name

class StartTime(models.Model):
    start_time_id = models.AutoField(primary_key=True)
    start_time = models.TimeField(verbose_name='Hora de Inicio')

    def __str__(self):
        if self.start_time.minute == 0:
            return str(self.start_time.hour)+'h'+'00'
        else:
            return str(self.start_time.hour)+'h'+str(self.start_time.minute)

class MatchDuration(models.Model):
    duration_id = models.AutoField(primary_key=True)
    duration = models.DurationField(verbose_name='Duracion')

    def __str__(self):
        time = self.duration + dt.timedelta(minutes=30)
        return 'h'.join(str(time).split(':')[:2])

class Reservation(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    start_time = models.ForeignKey(StartTime, on_delete=models.CASCADE, verbose_name='Hora de Inicio')
    duration = models.ForeignKey(MatchDuration, on_delete=models.CASCADE, verbose_name='Duracion')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Cliente',null=True, blank=True)
    court = models.ForeignKey(Court, on_delete=models.CASCADE, verbose_name='Cancha')
    date = models.DateField(blank=True,null=True, verbose_name='Fecha')

    def get_absolute_url(self):
        return reverse('reservations')

class FixedReservation(models.Model):
    fixed_reservation_id = models.AutoField(primary_key=True)
    fixed_start_time = models.ForeignKey(StartTime, on_delete=models.CASCADE, verbose_name='Hora de Inicio')
    fixed_duration = models.ForeignKey(MatchDuration, on_delete=models.CASCADE, verbose_name='Duracion')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Cliente',null=True, blank=True)
    fixed_court = models.ForeignKey(Court, on_delete=models.CASCADE, verbose_name='Cancha')
    fixed_date = models.CharField(choices=day_choices,max_length=15,blank=True,null=True, verbose_name='Fecha Fija')
