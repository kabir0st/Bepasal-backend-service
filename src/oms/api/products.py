from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from core.permissions import IsStaffOrReadOnly
from core.utils.viewsets import DefaultViewSet
from oms.api.serializers.product import (AdminProductListSerializer,
                                         CategorySerializer,
                                         ProductImageSerializer,
                                         ProductListSerializer,
                                         ProductSerializer,
                                         ProductVariationImageSerializer,
                                         ProductVariationSerializer,
                                         VariationOptionSerializer,
                                         VariationTypeSerializer)
from oms.models.product import (Category, Product, ProductImage,
                                ProductVariation, ProductVariationImage,
                                VariationOption, VariationType)


class CategoryAPI(DefaultViewSet):
    serializer_class = CategorySerializer
    search_fields = ["name"]
    permission_classes = [IsStaffOrReadOnly]
    queryset = Category.objects.filter().order_by('-id')


class ProductAPI(DefaultViewSet):
    serializer_class = ProductSerializer
    search_fields = ["name"]
    lookup_field = 'slug'
    permission_classes = [IsStaffOrReadOnly]
    queryset = Product.objects.filter().order_by('-id')

    def get_serializer_class(self):
        if self.action == 'list':
            if self.request.user.is_staff:
                return AdminProductListSerializer
            return ProductListSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            obj = serializer.save()
            data = request.data.copy()
            data['product'] = obj.id
            empty_variation_serializer = ProductVariationSerializer(
                instance=obj, data=data)
            empty_variation_serializer.is_valid(raise_exception=True)
            empty_variation_serializer.save()
        return Response(self.get_serializer(instance=obj).data,
                        status=status.HTTP_201_CREATED)


class ProductImageAPI(DefaultViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [IsStaffOrReadOnly]
    queryset = ProductImage.objects.filter().order_by('-id')


class VariationTypeOptionAPI(DefaultViewSet):
    serializer_class = VariationOptionSerializer
    permission_classes = [IsStaffOrReadOnly]
    queryset = VariationOption.objects.filter().order_by('-id')

    def get_queryset(self):
        id = self.kwargs.get('variation_pk', None)
        if id is None:
            return self.queryset.none()
        return self.queryset.filter(variation_type__id=id)


class VariationTypeAPI(DefaultViewSet):
    serializer_class = VariationTypeSerializer
    search_fields = ["name"]
    permission_classes = [IsStaffOrReadOnly]
    queryset = VariationType.objects.filter().order_by('-id')


class ProductVariationAPI(DefaultViewSet):
    serializer_class = ProductVariationSerializer
    search_fields = ["slug"]
    lookup_field = 'slug'
    permission_classes = [IsStaffOrReadOnly]
    queryset = ProductVariation.objects.filter().order_by('-id')

    def get_queryset(self):
        slug = self.kwargs.get('product_slug', None)
        if slug is None:
            return self.queryset.none()
        return self.queryset.filter(product__slug=slug)


class ProductVariationImageAPI(DefaultViewSet):
    serializer_class = ProductVariationImageSerializer
    permission_classes = [IsStaffOrReadOnly]
    queryset = ProductVariationImage.objects.filter().order_by('-id')

    def get_queryset(self):
        slug = self.kwargs.get('variation_slug', None)
        if slug is None:
            return self.queryset.none()
        return self.queryset.filter(product_variation__slug=slug)
