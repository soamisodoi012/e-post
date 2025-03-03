from django.db import models
from goodsAndItems.models import Category, Item
from customer.models import Customer
from locationManagement.models import Address
from django.utils.crypto import get_random_string
from django.db import models
from goodsAndItems.models import Item  # Assuming Category is not used in this model
from customer.models import Customer
from locationManagement.models import Address
from django.utils.crypto import get_random_string

class ShippingOrder(models.Model):
    STATUS_CHOICES = [
        ('onshipping', 'On Shipping'),
        ('delivered', 'Delivered'),
        ('onreviewing', 'On Reviewing'),
        ('reviewed', 'Reviewed'),
        ('pending', 'Pending'),]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.CharField()
    description=models.TextField()
    location1 = models.ForeignKey(Address, related_name='shipping_orders_from', on_delete=models.CASCADE)
    location2 = models.ForeignKey(Address, related_name='shipping_orders_to', on_delete=models.CASCADE)
    distance = models.FloatField()
    shipping_cost = models.FloatField()
    description=models.TextField()
    
    # Unique identifier based on customer, location1, and item
    shipId = models.CharField(max_length=255, unique=False, editable=False, primary_key=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='onreviewing')
