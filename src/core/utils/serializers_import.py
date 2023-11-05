import contextlib
from django.apps import apps
from rest_framework import serializers

serializer_classes = []

for app_config in apps.get_app_configs():
    with contextlib.suppress(ImportError):
        serializers_module = f"{app_config.module.__name__}.api.serializers"
        # Import the serializers module
        serializers_module = __import__(serializers_module, fromlist=["*"])

        # Iterate through the attributes of the serializers module
        for attr_name in dir(serializers_module):
            attr = getattr(serializers_module, attr_name)
            if isinstance(attr, type) and issubclass(attr,
                                                     serializers.Serializer):
                serializer_classes.append(attr)
