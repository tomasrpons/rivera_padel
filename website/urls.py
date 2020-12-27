from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('index/',views.index, name='index'),
    path('contact/',views.contact, name='contact'),
    path('reservations/',views.reservations, name='reservations'),
    path('book/', views.BookView.as_view(), name='book'),

    path('ajax/load_start_times/', views.load_start_times, name='ajax_load_start_times'), # AJAX
    path('ajax/load_durations/', views.load_durations, name='ajax_load_durations'), # AJAX

]
