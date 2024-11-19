from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=300,unique=True)
    password = models.CharField(max_length=300)
    email = models.EmailField()
    image = models.FileField()
    address = models.CharField(max_length=300)
    contact = models.CharField(max_length=300)

class ProductType(models.Model):
    name = models.CharField(max_length=300)

class Product(models.Model):
    name = models.CharField(max_length=300)
    image = models.FileField()
    description = models.TextField()
    stock = models.IntegerField()
    type = models.ForeignKey(ProductType,on_delete=models.SET_NULL,null=True)
    department = models.ManyToManyField('Department',null=True,blank=True)

class Purchase(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    vendor = models.ForeignKey('Vendor',on_delete=models.SET_NULL,null=True)

class Sell(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    customer_name = models.CharField(max_length=300)

class Department(models.Model):
    name = models.CharField(max_length=300)
    floor = models.CharField(max_length=20)

class Vendor(models.Model):
    name = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    contact = models.CharField(max_length=300)
    email = models.EmailField()