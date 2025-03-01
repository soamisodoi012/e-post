from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('addtoshiping/', views.add_to_shiping),
    path('addtoshipingorder/', views.process_order_ship),
    path('vieworder/',views.view_cart),
    
]