from uuid import uuid4

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models

from core.utils.models import TimeStampedModel


def default_array():
    return []


class UserbaseManager(BaseUserManager):

    def create_superuser(self, email, given_name, password, **other_fields):

        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must be assigned to is_superuser=True.")

        return self.create_user(email, given_name, password, **other_fields)

    def create_user(self, email, given_name, password, **other_fields):

        if not email:
            raise ValueError("You must provide an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, given_name=given_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class UserBase(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    uuid = models.UUIDField(unique=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    given_name = models.CharField(max_length=255, blank=True, default='')
    family_name = models.CharField(max_length=255, blank=True, default='')

    display_image = models.ImageField(upload_to='user_display_images',
                                      blank=True,
                                      null=True)
    phone_number = models.CharField(max_length=255, default='', blank=True)

    address = models.TextField(default='', blank=True)
    zip_code = models.CharField(max_length=255, blank=True, default='')
    city = models.CharField(max_length=255, blank=True, default='')
    country = models.CharField(max_length=255, blank=True, default='')

    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["given_name", "family_name"]

    objects = UserbaseManager()

    @property
    def full_name(self):
        return f"{self.given_name} {self.family_name}"

    def __str__(self):
        return f"{self.email}"

    class Meta:
        ordering = ["-id"]
