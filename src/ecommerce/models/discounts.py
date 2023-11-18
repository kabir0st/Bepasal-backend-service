from core.utils.models import TimeStampedModel
from django.db import models


class Discount(TimeStampedModel):
    name = models.CharField(max_length=255)
    discount_code = models.CharField(max_length=255, unique=True)
    discount_percent = models.DecimalField()
