from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.utils.text import slugify


def validate_image_size(value):
    # Limit the file size to 2 MB (2 * 1024 * 1024 bytes)
    max_size = 2 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError('File size must be less than 2 MB.')


class TimeStampedModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_active', '-id']
        abstract = True

    def save(self, *args, **kwargs):
        if hasattr(self, 'name'):
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        if hasattr(self, 'name'):
            return self.name
        return super().__str__()


class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        try:
            obj = cls.objects.get(id=1)
        except ObjectDoesNotExist:
            obj = cls.objects.create(id=1)
        return obj


class AbstractItemInfo(models.Model):
    selling_price = models.PositiveIntegerField(default=0)
    crossed_price = models.PositiveBigIntegerField(default=0)
    cost_price = models.PositiveIntegerField(default=0)
    quantity = models.IntegerField(default=0)
    sku = models.CharField(default='', max_length=255)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
