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
        if hasattr(self, 'slug'):
            return self.slug
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


class AbstractProductInfo(models.Model):
    selling_price = models.DecimalField(
        default=0.00, max_digits=60, decimal_places=2)
    crossed_price = models.DecimalField(
        default=0.00, max_digits=60, decimal_places=2)
    cost_price = models.DecimalField(
        default=0.00, max_digits=60, decimal_places=2)
    stock = models.DecimalField(default=0.00, max_digits=60, decimal_places=2)
    units = (('unit', 'unit'), ('kg', "kg"),
             ('g', "g"), ('l', "l"), ('ml', "ml"))
    stock_unit_in = models.CharField(max_length=25,
                                     choices=units,
                                     default='g')
    sku = models.CharField(default='', max_length=255)
    is_eligible_for_discount = models.BooleanField(default=True)

    tax_types = (('exclusive', 'exclusive'), ('inclusive', 'inclusive'))
    tax_type = models.CharField(max_length=25,
                                choices=tax_types,
                                default='exclusive')
    taxes_applied = models.ManyToManyField(
        'Tax', blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
