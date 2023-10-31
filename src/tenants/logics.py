import random
import string

from core.utils.functions import remove_spaces
from django.db import transaction
from django_tenants.utils import get_tenant_type_choices
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.viewsets import ModelViewSet
from tenants.models import Client, DeactivatedClient, Domain
from tenants.tasks import migrate_new_client
from rest_framework.exceptions import APIException


class ClientSerializer(ModelSerializer):

    domain = SerializerMethodField()

    class Meta:
        model = Client
        fields = '__all__'

    def get_domain(self, obj):
        domain = obj.domains.filter(is_primary=True).first()
        return domain.domain if domain else None


class InstanceAPI(ModelViewSet):
    queryset = Client.objects.filter()
    serializer_class = ClientSerializer
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        search = request.GET.get('search', None)
        queryset = self.filter_queryset(
            self.get_queryset()).exclude(schema_name='public')

        if search:
            queryset = queryset.filter(name__icontains=remove_spaces(search))
        response_json = {
            'status': True,
            'data': self.get_serializer(queryset, many=True).data,
            'count': queryset.count()
        }
        return Response(response_json, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data_json = request.data
        if Domain.objects.filter(domain=data_json['domain']).first():
            raise APIException(f'{data_json["domain"]} domain already in use.')

        if Client.objects.filter(name=data_json['name']).first():
            raise APIException(f"{data_json['name']} name already in use.")

        if Client.objects.filter(schema_name=data_json['schema_name']).first():
            raise APIException(
                f"{data_json['schema_name']} name already in use.")
        if data_json['type'] not in list(sum(get_tenant_type_choices(), ())):
            raise APIException(f'Type: {data_json["type"]} not found.')

        verification_code = ''.join(
            random.SystemRandom().choice(string.ascii_uppercase +
                                         string.digits) for _ in range(255))

        client = Client(schema_name=data_json['name'],
                        name=data_json['schema_name'],
                        type=data_json['type'],
                        verification_code=verification_code)
        client.save()
        data_json['id'] = client.id
        domain = Domain()
        domain.domain = data_json['domain']
        domain.tenant = client
        domain.save()
        res = {
            'domain': data_json['domain'],
            'verification_code': verification_code,
            'client_id': client.id,
        }
        migrate_new_client.delay(data_json)
        return Response(res, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response_json = {'status': True}
        return Response(response_json, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, *args, **kwargs):
        client = self.get_object()
        if request.GET.get('hardDelete', None):
            with transaction.atomic():
                client.delete()
            return Response({'status': True})
        with transaction.atomic():
            cl = DeactivatedClient.objects.filter(name=client.name)
            cl.delete()
            DeactivatedClient.objects.create(
                name=client.name, verification_code=client.verification_code)
            for de in client.domains.all():
                de.delete()
        return Response({'status': True})

    @action(methods=['get'], detail=True)
    def activate(self, request, *args, **kwargs):
        client = self.get_object()
        domain_str = request.GET.get('domain')
        with transaction.atomic():
            de_client = DeactivatedClient.objects.get(
                name=client.name, verification_code=client.verification_code)
            domain = Domain()
            domain.domain = domain_str
            domain.tenant = client
            domain.save()
            de_client.delete()
        return Response({'status': True})
