from django.db import models
from django_tenants.models import DomainMixin, TenantMixin
from django_tenants.utils import get_tenant_type_choices


class Client(TenantMixin):

    name = models.CharField(max_length=63, unique=True)
    verification_code = models.CharField(max_length=255)
    type = models.CharField(
        max_length=100, choices=get_tenant_type_choices())
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


class DeactivatedClient(models.Model):
    name = models.CharField(max_length=63, unique=True)
    verification_code = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Template(models.Model):
    name = models.CharField(max_length=255, unique=True)
    link = models.CharField(max_length=255, unique=True)
    description = models.TextField(default='')

    is_active = models.BooleanField(default=True)


class Domain(DomainMixin):
    pass
