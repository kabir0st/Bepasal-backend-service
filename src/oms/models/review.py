from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.utils.models import TimeStampedModel
from users.models.users import UserBase


def image_directory_path(instance, filename):
    return f"/reviews/{filename}"


class ReviewImage(TimeStampedModel):
    image = models.ImageField(upload_to=image_directory_path,
                              null=True,
                              blank=True)


class Review(TimeStampedModel):
    user = models.ForeignKey(
        UserBase, on_delete=models.CASCADE, related_name='reviews')
    images = models.ManyToManyField(ReviewImage)
    text = models.TextField(default='')
    stars = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(0), MaxValueValidator(10)])
