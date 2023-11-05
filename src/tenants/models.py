from django.db import models
from django_tenants.models import DomainMixin, TenantMixin
from django_tenants.utils import get_tenant_type_choices

from core.utils.models import TimeStampedModel


class Template(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    pre_fix = models.CharField(unique=True, max_length=255)


class Client(TenantMixin):

    name = models.CharField(max_length=63, unique=True)
    verification_code = models.CharField(max_length=255)
    template_used = models.ForeignKey(
        Template, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=100, choices=get_tenant_type_choices())

    created_on = models.DateField(auto_now_add=True)

    auto_create_schema = True

    def __str__(self):
        return f'{self.name}'


class DeactivatedClient(models.Model):
    name = models.CharField(max_length=63, unique=True)
    verification_code = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Domain(DomainMixin):
    pass
