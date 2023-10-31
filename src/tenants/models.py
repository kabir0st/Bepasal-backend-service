from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


class Client(TenantMixin):

    name = models.CharField(max_length=63, unique=True)
    verification_code = models.CharField(max_length=255)
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


class DeactivatedClient(models.Model):
    name = models.CharField(max_length=63, unique=True)
    verification_code = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Domain(DomainMixin):
    pass
