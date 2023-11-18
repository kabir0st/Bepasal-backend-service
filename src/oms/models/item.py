import contextlib
import os

from ckeditor.fields import RichTextField
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from PIL import Image

from core.utils.functions import optimize_image
from core.utils.models import AbstractItemInfo, TimeStampedModel


class Category(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(default='', null=True, blank=True)


def image_directory_path(instance, filename):
    return f"images/{instance.slug}/{filename}"


class VariationType(models.Model):
    name = models.CharField(max_length=255, unique=True)


class VariationOption(models.Model):
    name = models.CharField(max_length=255)
    variation_type = models.ForeignKey(
        VariationType, on_delete=models.CASCADE, related_name='options')


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = RichTextField()
    continue_selling_after_out_of_stock = models.BooleanField(default=True)
    catagories = models.ManyToManyField(Category, blank=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    thumbnail_image = models.ImageField(upload_to=image_directory_path,
                                        blank=True, null=True)
    enabled_variation_types = models.ManyToManyField(VariationType, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super(Item, self).save(*args, **kwargs)
        ItemVariation.objects.create(item=self)


class ItemVariation(AbstractItemInfo):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='variations')
    variation_option_combination = models.ManyToManyField(
        VariationOption, related_name='variations', blank=True)


@receiver(pre_save, sender=Item)
def handle_item_pre_save(sender, instance, *args, **kwargs):
    instance.trigger_gen = not bool(instance.id)
    if instance.id and instance.id != Item.objects.get(id=instance.id).name:
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


@receiver(post_save, sender=Item)
def handle_post_save_item(sender, instance, created, *args, **kwargs):
    if instance.trigger_gen:
        instance.slug = f"{slugify(instance.name)}-{instance.id}"
        pre_save.disconnect(handle_item_pre_save, sender=Item)
        post_save.disconnect(handle_post_save_item, sender=Item)
        instance.save()
        pre_save.connect(handle_item_pre_save, sender=Item)
        post_save.connect(handle_post_save_item, sender=Item)


class ItemImage(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=image_directory_path,
                              null=True,
                              blank=True)


@receiver(pre_save, sender=ItemImage)
def handle_item_image_pre_save(sender, instance, *args, **kwargs):
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


class ItemVariationImage(models.Model):
    item_variation = models.ForeignKey(
        ItemVariation, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=image_directory_path,
                              null=True,
                              blank=True)


@receiver(pre_save, sender=ItemVariationImage)
def handle_item_image_variation_pre_save(sender, instance, *args, **kwargs):
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
