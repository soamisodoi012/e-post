from django.db import models

# Create your models here.
class Address(models.Model):
    addresId=models.CharField(primary_key=True)
    addresName=models.CharField()
    latitude = models.FloatField(default=0)
    longitude = models.FloatField()
    street_address = models.TextField()  # Multiline support for street address
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)