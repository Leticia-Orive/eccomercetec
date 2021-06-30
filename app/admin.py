from django.contrib import admin

# Register your models here.
from .models import Product, Category, Manufacturer, Profile, Order
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Manufacturer)
admin.site.register(Profile)
admin.site.register(Order)