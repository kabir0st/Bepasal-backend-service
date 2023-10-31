from core.celery import celery_app
from django.db import transaction
from django_tenants.utils import tenant_context
from tenants.models import Client


@celery_app.task
def migrate_new_client(data_json):
    with transaction.atomic():
        client = Client.objects.get(id=data_json['id'])
        with tenant_context(client):
            pass
