from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('index/',views.index, name='index'),
    path('contact/',views.contact, name='contact'),
    path('reservations/',views.reservations, name='reservations'),
    path('book/', views.BookView.as_view(), name='book'),

]