from django.db import models

from core.utils.functions import default_json
from core.utils.models import TimeStampedModel
from oms.models.item import Item, ItemVariation
from users.models.users import UserBase


class Order(TimeStampedModel):
    user = models.ForeignKey(
        UserBase, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='orders')
    user_name = models.CharField(max_length=255, default='')
    user_contact = models.CharField(max_length=255, default='')

    delivery_note = models.CharField(max_length=255, default='')
    delivery_location = models.CharField(max_length=255, default='')
    geo_tag = models.JSONField(default=default_json)

    # prices
    total_price = models.DecimalField(null=True,
                                      blank=True,
                                      max_digits=60,
                                      decimal_places=2)
    total_discount_amount = models.DecimalField(null=True,
                                                blank=True,
                                                max_digits=60,
                                                decimal_places=2)
    extra_discount = models.DecimalField(null=True,
                                         blank=True,
                                         max_digits=60,
                                         decimal_places=2)
    discount_remarks = models.CharField(max_length=255, default='')
    total_bill_amount = models.DecimalField(null=True,
                                            blank=True,
                                            max_digits=60,
                                            decimal_places=2)
    total_amount_paid = models.DecimalField(null=True,
                                            blank=True,
                                            max_digits=60,
                                            decimal_places=2)

    def __str__(self, instance):
        return f'{instance.user}' if instance.user else instance.user_name


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items')
    item_instance = models.ForeignKey(
        Item, on_delete=models.PROTECT, related_name='order_items')
    variation = models.ForeignKey(
        ItemVariation, on_delete=models.PROTECT, related_name='order_items')

    item_name = models.CharField(max_length=255)
    variation = models.CharField(max_length=255)

    price = models.DecimalField(null=True,
                                blank=True,
                                max_digits=60,
                                decimal_places=2)
    discount_amount = models.DecimalField(null=True,
                                          blank=True,
                                          max_digits=60,
                                          decimal_places=2)
    discount_remarks = models.CharField(max_length=255, default='')
    bill_amount = models.DecimalField(null=True,
                                      blank=True,
                                      max_digits=60,
                                      decimal_places=2)

    def __str__(self, instance):
        return f'''{instance.order}
        {instance.order if instance.item_instance else instance.item_name }'''
