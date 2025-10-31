from django.db import models

class Cheque(models.Model):
    image = models.ImageField(upload_to='cheques/')
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payee = models.CharField(max_length=255)
