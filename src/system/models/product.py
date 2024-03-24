import contextlib
import os
import random

from ckeditor.fields import RichTextField
from django.db import models
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from django.forms import ValidationError
from django.utils.text import slugify
from PIL import Image

from core.utils.functions import optimize_image
from core.utils.models import AbstractProductInfo


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, blank=True, default='')
    description = models.TextField(default='', null=True, blank=True)
    parent_category = models.ForeignKey(
        'Category', on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        ordering = ['-id']

    def save(self, *args, **kwargs):
        if hasattr(self, 'name'):
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        if hasattr(self, 'name'):
            return self.name
        if hasattr(self, 'slug'):
            return self.slug
        return super().__str__()


def image_directory_path(instance, filename):
    return f"images/{instance.slug}/{filename}"


class VariationType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        if hasattr(self, 'name'):
            return self.name
        if hasattr(self, 'slug'):
            return self.slug
        return super().__str__()


class VariationOption(models.Model):
    name = models.CharField(max_length=255)
    variation_type = models.ForeignKey(
        VariationType, on_delete=models.CASCADE, related_name='options')

    def __str__(self):
        return f"{self.variation_type} {self.name}"


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = RichTextField()
    categories = models.ManyToManyField(Category, blank=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    thumbnail_image = models.ImageField(upload_to=image_directory_path,
                                        blank=True, null=True)
    enabled_variation_types = models.ManyToManyField(VariationType, blank=True)
    default_variant = models.ForeignKey(
        'ProductVariation', on_delete=models.SET_NULL,
        null=True, blank=True, default=None, related_name='default_product')
    continue_selling_after_out_of_stock = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


@receiver(pre_save, sender=Product)
def handle_product_pre_save(sender, instance, *args, **kwargs):
    instance.slug = f"{slugify(instance.name)}"
    if instance.default_variant:
        if instance.default_variant.product != instance:
            raise ValidationError(
                "Default variant must be a variant of selected product.")
    if instance.thumbnail_image:
        with contextlib.suppress(Exception):
            image_name = instance.thumbnail_image.name
            if not image_name.endswith('.webp'):
                if "/" in instance.thumbnail_image.name:
                    image_name = instance.thumbnail_image.name.split('/')[-1]
                temp_output_image_path = f"temp_{image_name}"
                with instance.thumbnail_image.open("rb") as image_file:
                    image = Image.open(image_file)
                    optimized_image_path = optimize_image(
                        image, temp_output_image_path)
                with open(optimized_image_path, "rb") as optimized_image_file:
                    instance.thumbnail_image.save(image_name.replace(
                        image_name.split('.')[-1], 'webp'),
                        optimized_image_file,
                        save=False)
                os.remove(optimized_image_path)


def file_directory_path(instance, filename):
    return f"digital_files/{instance.product.slug}/{filename}"


def image_directory_path2(instance, filename):
    return f"images/{instance.product.slug}/{filename}"


class ProductVariation(AbstractProductInfo):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='variations')
    variation_option_combination = models.ManyToManyField(
        VariationOption, related_name='variations', blank=True)

    thumbnail_image = models.ImageField(upload_to=image_directory_path2,
                                        blank=True, null=True)
    is_eligible_for_discounts = models.BooleanField(default=True)
    is_digital = models.BooleanField(default=False)
    auto_complete_digital_orders = models.BooleanField(default=True)
    digital_file = models.FileField(upload_to=file_directory_path,
                                    blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        variation_combination = [
            str(option) for option in (
                self.variation_option_combination.filter())
        ]
        return f"{self.product} {' '.join(variation_combination)}"


@receiver(
    m2m_changed, sender=ProductVariation.variation_option_combination.through)
def handle_variation_option_combination_change(
        sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        variation_combination = [
            option.name for option in (
                instance.variation_option_combination.all())
        ]
        if not variation_combination:
            variation_combination = [str(random.randint(10000, 99999))]
        instance.slug = slugify(
            f"{instance.product}-{' '.join(variation_combination)}")
        instance.save()


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=image_directory_path2,
                              null=True,
                              blank=True)


@receiver(pre_save, sender=ProductImage)
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


def image_directory_path3(instance, filename):
    return f"images/{instance.product_variation.product.slug}/{filename}"


class ProductVariationImage(models.Model):
    product_variation = models.ForeignKey(
        ProductVariation, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=image_directory_path3,
                              null=True,
                              blank=True)


@receiver(pre_save, sender=ProductVariationImage)
def handle_product_image_variation_pre_save(sender, instance, *args, **kwargs):
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
