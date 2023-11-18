from django.db import models
from oms.models.item import ItemVariation

from users.models.users import UserBase


class Cart(models.Model):
    user = models.ForeignKey(UserBase, on_delete=models.CASCADE, unique=True)
    items = models.ManyToManyField(ItemVariation, blank=True)
