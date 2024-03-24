import os
from PIL import Image
from core.utils.functions import default_json, optimize_image
import contextlib
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from system.models.product import Product, ProductVariation
from users.models.users import UserBase


# to implement cart abandoned by user calculated use updated_at
class Cart(models.Model):
    user = models.OneToOneField(UserBase, on_delete=models.CASCADE)
    product_variations = models.ManyToManyField(
        ProductVariation)
    quantities = models.JSONField(default=default_json, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ReviewImage(models.Model):
    image = models.ImageField(upload_to='review_images',
                                        blank=True, null=True)


@receiver(pre_save, sender=ReviewImage)
def handle_product_image_pre_save(sender, instance, *args, **kwargs):
    if instance.image:
        with contextlib.suppress(Exception):
            image_name = instance.image.name
            if not image_name.endswith('.webp'):
                if "/" in instance.image.name:
                    image_name = instance.image.name.split('/')[-1]
                temp_output_image_path = f"temp_{image_name}"
                with instance.image.open("rb") as image_file:
                    image = Image.open(image_file)
                    optimized_image_path = optimize_image(
                        image, temp_output_image_path)
                with open(optimized_image_path, "rb") as optimized_image_file:
                    instance.image.save(image_name.replace(
                        image_name.split('.')[-1], 'webp'),
                        optimized_image_file,
                        save=False)
                os.remove(optimized_image_path)


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


class QA(models.Model):
    user = models.ForeignKey(UserBase, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    question = models.TextField(default='')
    answer = models.TextField(default='', blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='qas')


@receiver(pre_save, sender=QA)
def handle_qa_pre_save(sender, instance, *args, **kwargs):
    if instance.user:
        instance.name = instance.user.full_name


class WishList(models.Model):
    user = models.OneToOneField(UserBase, on_delete=models.CASCADE)
    product_variations = models.ManyToManyField(
        ProductVariation, blank=True)
