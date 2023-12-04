import contextlib
import os

from ckeditor.fields import RichTextField
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
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
    name = models.CharField(max_length=255)
    description = RichTextField()
    categories = models.ManyToManyField(Category, blank=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    thumbnail_image = models.ImageField(upload_to=image_directory_path,
                                        blank=True, null=True)
    enabled_variation_types = models.ManyToManyField(VariationType, blank=True)

    is_item_digital = models.BooleanField(default=False)
    continue_selling_after_out_of_stock = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


def file_directory_path(instance, filename):
    return f"digital_files/{instance.product.slug}/{filename}"


class ProductVariation(AbstractProductInfo):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='variations')
    variation_option_combination = models.ManyToManyField(
        VariationOption, related_name='variations', blank=True)

    is_default_variation = models.BooleanField(default=False)
    is_eligible_for_discounts = models.BooleanField(default=True)

    auto_complete_digital_orders = models.BooleanField(default=True)
    digital_file = models.FileField(upload_to=file_directory_path,
                                    blank=True, null=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        variation_combination = [
            str(option) for option in (
                self.variation_option_combination.filter())
        ]
        return f"{self.product} {' '.join(variation_combination)}"

    def save(self, *args, **kwargs) -> None:
        self.trigger_gen = None
        return super().save(*args, **kwargs)


@receiver(pre_save, sender=Product)
def handle_product_pre_save(sender, instance, *args, **kwargs):
    instance.trigger_gen = not bool(instance.id)
    if instance.id and instance.id != Product.objects.get(id=instance.id).name:
        instance.trigger_gen = True
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


@receiver(post_save, sender=Product)
def handle_post_save_product(sender, instance, created, *args, **kwargs):
    if instance.trigger_gen:
        instance.slug = f"{slugify(instance.name)}-{instance.id}"
        pre_save.disconnect(handle_product_pre_save, sender=Product)
        post_save.disconnect(handle_post_save_product, sender=Product)
        instance.save()
        pre_save.connect(handle_product_pre_save, sender=Product)
        post_save.connect(handle_post_save_product, sender=Product)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=image_directory_path,
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


class ProductVariationImage(models.Model):
    product_variation = models.ForeignKey(
        ProductVariation, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=image_directory_path,
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
