
from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from tenants.models import Client, Domain, Template


@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(Domain)


@admin.register(Template)
class TemplateAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'link')
