from django.db import models

from core.utils.functions import default_json
from core.utils.models import TimeStampedModel
from oms.models.product import ProductVariation
from users.models.users import UserBase


class OrderStatus(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    subtract_from_inventory = models.BooleanField(default=True)


class DeliveryMethod(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)


class Order(TimeStampedModel):
    user = models.ForeignKey(
        UserBase, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='orders')
    user_name = models.CharField(max_length=255, default='', blank=True)
    user_contact = models.CharField(max_length=255, default='', blank=True)
    backup_contact = models.CharField(max_length=255, default='', blank=True)
    status = models.ForeignKey(
        OrderStatus, related_name='orders', on_delete=models.PROTECT)
    # prices
    total_price = models.DecimalField(max_digits=60,
                                      decimal_places=2,
                                      default=0.00)
    total_discount_amount = models.DecimalField(max_digits=60,
                                                decimal_places=2,
                                                default=0.00)
    extra_discount = models.DecimalField(max_digits=60,
                                         decimal_places=2,
                                         default=0.00)
    discount_remarks = models.CharField(max_length=255, default='')
    total_bill_amount = models.DecimalField(max_digits=60,
                                            decimal_places=2,
                                            default=0.00)
    total_amount_paid = models.DecimalField(max_digits=60,
                                            decimal_places=2,
                                            default=0.00)
    is_refunded = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)

    cancellation_remarks = models.TextField(default='', blank=True)
    refunded_remarks = models.TextField(default='', blank=True)

    delivery_method = models.ForeignKey(
        DeliveryMethod, on_delete=models.SET_NULL, null=True, blank=True)

    extra_fields = models.JSONField(default=default_json)

    delivery_note = models.CharField(max_length=255, default='', blank=True)
    delivery_location = models.CharField(
        max_length=255, default='', blank=True)
    geo_tag = models.JSONField(default=default_json, blank=True)

    def __str__(self, instance):
        return f'{instance.user}' if instance.user else instance.user_name


class OrderItemStatus(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    subtract_from_inventory = models.BooleanField(default=True)


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(
        ProductVariation, on_delete=models.PROTECT, related_name='order_items')

    product_name = models.CharField(max_length=255)
    variation = models.CharField(max_length=255)

    price = models.DecimalField(max_digits=60,
                                decimal_places=2,
                                default=0.00)
    discount_amount = models.DecimalField(max_digits=60,
                                          decimal_places=2,
                                          default=0.00)
    discount_remarks = models.CharField(max_length=255, default='')
    bill_amount = models.DecimalField(max_digits=60,
                                      decimal_places=2,
                                      default=0.00)

    is_refunded = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)

    cancelled_remarks = models.TextField(default='', blank=True)
    returned_remarks = models.TextField(default='', blank=True)
    refunded_remarks = models.TextField(default='', blank=True)
