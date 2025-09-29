from django.contrib import admin

from inventory.models import Order, Product

admin.site.register(Order)

admin.site.register(Product)