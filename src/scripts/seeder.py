
from django.contrib.auth import get_user_model
from django_tenants.utils import tenant_context

from tenants.models import Client, Domain, Template


def seeder():
    prefix = 'http'
    main = 'localhost'

    templates = [
        'template-1', 'template-2'
    ]
    clients = [{
        'name': "Client 1",
        'slug': 'client1',
        'template': 'template-1',
        'url': f'{prefix}://client1.{main}:8000',

    }, {
        'name': "Client 2",
        'slug': 'client2',
        'template': 'template-2',
        'url': f'{prefix}://client2.{main}:8000',

    }]

    client = Client(schema_name='public', name='landlord')
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
        for template in templates:
            Template.objects.create(
                name=template,
                pre_fix=template
            )

    # for data in clients:
    #     client = Client(schema_name=data['slug'],
    #                     name=data['name'])
    #     client.save()
    #     domain = Domain()
    #     domain.domain = f'{data["url"]}'
    #     domain.tenant = client
    #     domain.save()

    #     with tenant_context(client):
    #         user_class = get_user_model()
    #         admin = user_class.objects.create_superuser('admin', '', 'pass')
    #         admin.save()
