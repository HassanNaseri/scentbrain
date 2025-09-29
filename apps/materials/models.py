from django.db import models


class Material(models.Model):
    CAS = models.CharField("CAS Registry number", max_length=12, blank=True, default="")
    name = models.CharField("Product name in invoice", max_length=500)
    is_syntetic = models.BooleanField(default=True)
    IFRA_NCS_category = models.CharField("IFRA naturals (NCS) category", max_length=12, blank=True, default="")
    synonyms = models.CharField("Product name in invoice", max_length=500)
    # ...
    def __str__(self):
        return self.name 


class IFRA_NCS_Letter(models.Model):  
    code = models.CharField("IFRA NCS code - letter part", max_length=1, blank=True, default="")
    description = models.CharField("CAS Registry Number", max_length=50, blank=True, default="")
    example = models.CharField("xxx", max_length=255, blank=True, default="")
    comment = models.CharField("xxx", max_length=255, blank=True, default="")
    def __str__(self):
        return self.code
    
    
class IFRA_NCS_Number(models.Model):
    code = models.CharField("IFRA NCS code - number part", max_length=8, blank=True, default="")
    description = models.CharField("CAS Registry Number", max_length=255, blank=True, default="")
    example = models.CharField("xxx", max_length=255, blank=True, default="")
    def __str__(self):
        return self.code