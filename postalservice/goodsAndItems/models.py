from django.db import models
class Category(models.Model):
    catName=models.CharField(max_length=100)
    catCode=models.CharField(primary_key=True)
class Item(models.Model):
    itemName=models.CharField()
    itemCode=models.CharField(primary_key=True)
   # catName=models.ForeignKey(Category,on_delete=models.CASCADE)
    catName=models.CharField()