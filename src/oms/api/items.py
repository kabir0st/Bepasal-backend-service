from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from core.permissions import IsAdminOrReadOnly
from core.utils.viewsets import DefaultViewSet
from oms.api.serializers.item import (CategorySerializer, ItemImageSerializer,
                                      ItemSerializer,
                                      ItemVariationImageSerializer,
                                      ItemVariationSerializer,
                                      VariationOptionSerializer,
                                      VariationTypeSerializer)
from oms.models.item import (Category, Item, ItemImage, ItemVariation,
                             ItemVariationImage, VariationOption,
                             VariationType)


class CategoryAPI(DefaultViewSet):
    serializer_class = CategorySerializer
    search_fields = ["name"]
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.filter().order_by('-id')


class ItemAPI(DefaultViewSet):
    serializer_class = ItemSerializer
    search_fields = ["name"]
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    queryset = Item.objects.filter().order_by('-id')

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            obj = serializer.save()
            data = request.data.copy()
            data['item'] = obj.id
            empty_variation_serializer = ItemVariationSerializer(
                instance=obj, data=data)
            empty_variation_serializer.is_valid(raise_exception=True)
            empty_variation_serializer.save()
        return Response(self.get_serializer(instance=obj).data,
                        status=status.HTTP_201_CREATED)


class ItemImageAPI(DefaultViewSet):
    serializer_class = ItemImageSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = ItemImage.objects.filter().order_by('-id')


class VariationTypeOptionAPI(DefaultViewSet):
    serializer_class = VariationOptionSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = VariationOption.objects.filter().order_by('-id')

    def get_queryset(self):
        id = self.kwargs.get('variation_pk', None)
        if id is None:
            return self.queryset.none()
        return self.queryset.filter(variation_type__id=id)


class VariationTypeAPI(DefaultViewSet):
    serializer_class = VariationTypeSerializer
    search_fields = ["name"]
    permission_classes = [IsAdminOrReadOnly]
    queryset = VariationType.objects.filter().order_by('-id')


class ItemVariationAPI(DefaultViewSet):
    serializer_class = ItemVariationSerializer
    search_fields = ["slug"]
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    queryset = ItemVariation.objects.filter().order_by('-id')

    def get_queryset(self):
        slug = self.kwargs.get('item_slug', None)
        if slug is None:
            return self.queryset.none()
        return self.queryset.filter(item__slug=slug)


class ItemVariationImageAPI(DefaultViewSet):
    serializer_class = ItemVariationImageSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = ItemVariationImage.objects.filter().order_by('-id')

    def get_queryset(self):
        slug = self.kwargs.get('variation_slug', None)
        if slug is None:
            return self.queryset.none()
        return self.queryset.filter(item_variation__slug=slug)
