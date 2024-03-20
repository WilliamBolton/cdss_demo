from django.db import models

# Create your models here.
class Vitals_plot(models.Model):
    metric = models.CharField(max_length=255)
    zero = models.DecimalField(decimal_places=2, max_digits=10)
    one = models.DecimalField(decimal_places=2, max_digits=10)
    two = models.DecimalField(decimal_places=2, max_digits=10)
    three = models.DecimalField(decimal_places=2, max_digits=10)
    four = models.DecimalField(decimal_places=2, max_digits=10)
    five = models.DecimalField(decimal_places=2, max_digits=10)
    six = models.DecimalField(decimal_places=2, max_digits=10)
    seven = models.DecimalField(decimal_places=2, max_digits=10)
