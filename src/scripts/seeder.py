
from django.contrib.auth import get_user_model
from django_tenants.utils import tenant_context
from core.utils.functions import client_has_app

from tenants.models import Client, Domain
from oms.models import OrderItemStatus, OrderStatus


def seeder():
    prod = True
    main = 'localhost' if not prod else 'himalayancreatives.com'

    clients = [{
        'name': "Client 2",
        'slug': 'client2',
        'url': f'oms.{main}',
        'type': 'oms'

    }, {
        'name': "Client 3",
        'slug': 'client3',
        'url': f'ecom.{main}',
        'type': 'ecommerce'

    }]

    client = Client(schema_name='public', name='landlord', type='public')
    client.save()
    print(client)
    domain = Domain()
    domain.domain = f'landlord.{main}'
    domain.tenant = client
    domain.is_primary = True
    domain.save()

    with tenant_context(client):
        user_class = get_user_model()
        admin = user_class.objects.create_superuser('super_admin', '', 'pass')
        admin.save()

    for data in clients:
        client = Client(schema_name=data['slug'],
                        name=data['name'], type=data['type'])
        client.save()
        domain = Domain()
        domain.domain = f'{data["url"]}'
        domain.tenant = client
        domain.save()

        with tenant_context(client):
            user_class = get_user_model()
            admin = user_class.objects.create_superuser('admin', '', 'pass')
            admin.save()
            status = ['Initiated', 'Processing',
                      'Sent for delivery', 'Delivered']
            if client_has_app('oms'):
                status_entries = (OrderStatus(
                    name=f"{s_name}") for s_name in status)
                OrderStatus.objects.bulk_create(list(status_entries))
                status_entries = (OrderItemStatus(
                    name=f"{s_name}") for s_name in status)
                OrderItemStatus.objects.bulk_create(list(status_entries))
                status = OrderItemStatus.objects.get(name='Initiated')
                status.subtract_from_inventory = False
                status.save()
                status = OrderStatus.objects.get(name='Initiated')
                status.subtract_from_inventory = False
                status.save()
