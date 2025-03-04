from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('createCategory/', views.createCategory),
    path('getCatById/', views.getCatById),
    path('createItem/', views.createItem),
   path('getItemById/', views.getItemById), 
   path('deleteCategory/', views.deleteCategory),
   path('deleteItem/', views.getItemById), 
]