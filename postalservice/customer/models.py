from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.hashers import make_password
class Customer(models.Model):
    username = models.EmailField(primary_key=True, unique=True)
    phone_number = PhoneNumberField(region='ET')
    faydaNumber=models.CharField()
    password = models.CharField(max_length=128)  # Store hashed passwords

    def save(self, *args, **kwargs):
       #hash the password
        self.password = make_password(self.password)
        super().save(*args, **kwargs)