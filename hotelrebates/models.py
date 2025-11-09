from django.db import models

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=100)
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
    
class Bank(models.Model):
    name = models.CharField(max_length=100)
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
    
class Currency(models.Model):
    name = models.CharField(max_length=100)
    cpp = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return self.name