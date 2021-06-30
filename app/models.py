from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "categories"

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)
    image = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "manufacturers"

    def __str__(self):
        return self.name


class Product(models.Model):
    manufacturer = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    ram = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    image = models.CharField(max_length=100)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    manufacturers = models.ManyToManyField(Manufacturer)

    class Meta:
        db_table = "products"

    def __str__(self):
        return self.manufacturer + " - " + self.model


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)

    class Meta:
        db_table = "profiles"

    def __str__(self):
        return self.user + " - " + self.type


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    date_order = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "orders"

    def __str__(self):
        return self.user + " - " + self.product



