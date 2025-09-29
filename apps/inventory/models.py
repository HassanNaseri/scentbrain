from django.db import models

# Create your models here.

# def get_currencies():
#     return {i: i for i in settings.CURRENCIES}

# def get_quantity_units():
#     return {i: i for i in settings.QUANTITY_UNITS}

CURRENCIES = {
    "USD": "USD",
    "GBP": "GBP",
    "EUR": "EUR",
}

QUANTITY_UNITS = {
    "g": "Gram",
    "ml": "Milliliter",
}

class Order(models.Model):
    supplier = models.CharField(max_length=200)
    delivery_date = models.DateField("delivery date", null=True)
    # ...
    def __str__(self):
        return f'{self.supplier} - {self.delivery_date.strftime("%Y-%m-%d")}'   
    
class Product(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    code = models.CharField("Product code in invoice", max_length=40, blank=True, default="")
    CAS = models.CharField("CAS Registry Number", max_length=12, blank=True, default="")
    name = models.CharField("Product name in invoice", max_length=100)
    manufacturer = models.CharField("Manufacturer of the product", max_length=100, blank=True, default="")
    dilution = models.PositiveSmallIntegerField("Dilution in percentage (1-100)", blank=True, default="100")
    solvent = models.CharField("Solvent used for diluting", max_length=100, blank=True, default="")
    quantity = models.DecimalField("Quantity - a number in a given unit", max_digits=4, decimal_places=1)
    quantity_unit = models.CharField("Unit of measuring quantity (mg, ml, ...)", max_length=2, choices=QUANTITY_UNITS)
    unit_price = models.DecimalField("Price for a unit of item ", max_digits=10, decimal_places=2, blank=True, null=True)
    price = models.DecimalField("Total price of item", max_digits=10, decimal_places=2)
    currency = models.CharField("Currency", max_length=3, choices=CURRENCIES)
    comments = models.CharField("Comments for the item in invoice", max_length=255, blank=True, default="")
    test_by_date = models.DateTimeField("Expiration or re-testing date for product", blank=True, null=True)
    # ...
    def __str__(self):
        return self.product_name    




    
    
    	