from django.db import models

from core.utils.models import SingletonModel


class SiteSettings(SingletonModel):
    name = models.CharField(max_length=255)
