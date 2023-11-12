from ckeditor.fields import RichTextField
from django.db import models
from django.utils.text import slugify

from core.utils.models import AbstractItemInfo, TimeStampedModel


class Category(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)


def image_directory_path(instance, filename):
    return f"/images/{instance.slug}/{filename}"


class Item(AbstractItemInfo):
    name = models.CharField(max_length=255)
    description = RichTextField()
    continue_selling_after_out_of_stock = models.BooleanField(default=True)
    catagories = models.ManyToManyField(Category)
    slug = models.CharField(max_length=255)
    thumbnail_image = models.ImageField(upload_to=image_directory_path)

    def save(self, *args, **kwargs):
        self.slug = f"{slugify(self.name)}"
        if Item.objects.filter(slug=self.slug).exclude(id=self.id).exists():
            self.slug = f"{self.slug}-{self.id}"


class ItemImage(TimeStampedModel):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=image_directory_path,
                              null=True,
                              blank=True)


class VariationType(TimeStampedModel):
    name = models.CharField(max_length=255, default='')
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='variation_types')

    class Meta:
        unique_together = ('item', 'name')

    def __str__(self):
        return f"{self.name}"


class ItemVariation(TimeStampedModel):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='variations')
    variation_type = models.ForeignKey(
        VariationType, on_delete=models.PROTECT, related_name='variations')
    slug = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.slug = f"{slugify(self.slug)-{self.variation}}"


class ItemVariationImage(TimeStampedModel):
    item_variation = models.ForeignKey(
        ItemVariation, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=image_directory_path,
                              null=True,
                              blank=True)
