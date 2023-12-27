from django.db import models


class Tax(models.Model):
    name = models.CharField(max_length=255, unique=True)
    rate = models.DecimalField(
        default=0.00, max_digits=60, decimal_places=2)
    rate_types = (('fixed', 'fixed'), ('percent', 'percent'))
    rate_type = models.CharField(max_length=25,
                                 choices=rate_types,
                                 default='percent')

    def __str__(self):
        return f'{self.name}'
