from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('index/',views.index, name='index'),
    path('contact/',views.contact, name='contact'),
    path('reservations/',views.reservations, name='reservations'),

    path('ajax/load_start_times/', views.load_start_times, name='ajax_load_start_times'), # AJAX
    path('ajax/load_durations/', views.load_durations, name='ajax_load_durations'), # AJAX
    
    path('ajax/load_fixed_start_times/', views.load_fixed_start_times, name='ajax_load_fixed_start_times'), # AJAX
    path('ajax/load_fixed_durations/', views.load_fixed_durations, name='ajax_load_fixed_durations'), # AJAX

    path('delete_reservation/<str:pk>/', views.delete_reservation, name='delete_reservation'),
    path('delete_fixed_reservation/<str:pk>/', views.delete_fixed_reservation, name='delete_fixed_reservation'),


]
