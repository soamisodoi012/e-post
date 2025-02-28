from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
class Customer(models.Model):
    username=models.EmailField(primary_key=True,unique=True)
    phone_number = PhoneNumberField(region='ET')