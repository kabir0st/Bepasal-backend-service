from core.utils.models import TimeStampedModel
from django.db import models


class Discount(TimeStampedModel):
    name = models.CharField(max_length=255)
    discount_code = models.CharField(max_length=255, unique=True)
    discount_percent = models.DecimalField(max_digits=60,
                                           decimal_places=2,
                                           default=0.00)

    def __str__(self):
        return f'{self.name}'
