from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from oms.models.product import Product, ProductVariation
from users.models.users import UserBase


# to implement cart abandoned by user calculated use updated_at
class Cart(models.Model):
    user = models.OneToOneField(UserBase, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    product_variation = models.ForeignKey(
        ProductVariation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class ReviewImage(models.Model):
    image = models.ImageField(upload_to='review_images',
                                        blank=True, null=True)


class Review(models.Model):
    user = models.ForeignKey(UserBase, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(10)])
    images = models.ManyToManyField(
        ReviewImage,  blank=True)


@receiver(pre_save, sender=Review)
def handle_review_pre_save(sender, instance, *args, **kwargs):
    if instance.user:
        instance.name = instance.user.full_name
