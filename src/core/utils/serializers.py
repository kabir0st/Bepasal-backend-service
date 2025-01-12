import base64
import uuid
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.exceptions import APIException


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        try:
            if data.startswith('data:image'):
                # base64 encoded image - decode
                format_, imgstr = data.split(';base64,')
                ext = format_.split('/')[-1]
                name = uuid.uuid4()
                data = ContentFile(base64.b64decode(imgstr),
                                   name=f'{name}.{ext}')
        except Exception as exp:
            raise APIException(f'Invalid Base64 format. {exp}') from exp
        return super().to_internal_value(data)

    def get_attribute(self, instance):
        # Override get_attribute to handle the case when the field is None
        value = instance
        for attr in self.source_attrs:
            if value is None:
                break
            value = getattr(value, attr, None)
        return value


class Base64FileField(serializers.FileField):

    def to_internal_value(self, data):
        try:
            _, imgstr = data.split(';base64,')
            ext = 'gpx'
            name = uuid.uuid4()
            data = ContentFile(base64.b64decode(imgstr), name=f'{name}.{ext}')
        except Exception as exp:
            raise APIException(f'Invalid Base64 format. {exp}') from exp
        return super().to_internal_value(data)
