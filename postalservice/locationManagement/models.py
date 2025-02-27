from django.db import models

# Create your models here.
class Address(models.Model):
    addresId=models.CharField(primary_key=True)
    addresName=models.CharField()
    distance=models.FloatField()