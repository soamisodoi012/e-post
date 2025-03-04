from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('createCustomer/', views.createCustomer),
    path('updateCustomer/',views.updateCustomer),
    path('getById/',views.getById)
]