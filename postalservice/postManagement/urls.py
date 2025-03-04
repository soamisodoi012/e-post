from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('addtoshiping/', views.add_to_shiping),
    path('addtoshipingorder/', views.process_order_ship),
    path('viewshipcart/',views.view_cart),
    path('vieworder/',views.review_order),
    path('review/',views.review),
    path('remove_from_shiping_cart/',views.remove_from_shiping_cart),
    path('customerHistory/',views.customerHistory),
    path('onshipping/',views.onshipping), 
    path('delivered/',views.delivered),
    
    
]