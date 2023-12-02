from django.db import models
from oms.models.product import ProductVariation

from users.models.users import UserBase


class Cart(models.Model):
    user = models.ForeignKey(UserBase, on_delete=models.CASCADE, unique=True)
    products = models.ManyToManyField(ProductVariation, blank=True)
