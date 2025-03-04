from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('createAdress/', views.createAdress),
    path('getAddress/',views.getAddress)
]