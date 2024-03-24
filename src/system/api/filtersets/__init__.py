from django_filters import FilterSet, CharFilter
from system.models import Product
from system.models.product import (
    Category, ProductVariation,
    VariationOption, VariationType
)
from rest_framework.exceptions import APIException


class ProductFilter(FilterSet):
    exclude = CharFilter(method='filter_exclude', label='Exclude Filter')

    class Meta:
        model = Product
        exclude = ('thumbnail_image',)

    def filter_exclude(self, queryset, name, value):
        try:
            exclude_ids = [int(id) for id in value.split(',')]
        except Exception:
            raise APIException('Invalid values in ?exclude filter.')
        return queryset.exclude(id__in=exclude_ids)


class CategoryFilter(FilterSet):
    exclude = CharFilter(method='filter_exclude', label='Exclude Filter')

    class Meta:
        model = Category
        fields = '__all__'

    def filter_exclude(self, queryset, name, value):
        try:
            exclude_ids = [int(id) for id in value.split(',')]
        except Exception:
            raise APIException('Invalid values in ?exclude filter.')
        return queryset.exclude(id__in=exclude_ids)


class VariationOptionFilter(FilterSet):
    exclude = CharFilter(method='filter_exclude', label='Exclude Filter')

    class Meta:
        model = VariationOption
        fields = '__all__'

    def filter_exclude(self, queryset, name, value):
        try:
            exclude_ids = [int(id) for id in value.split(',')]
        except Exception:
            raise APIException('Invalid values in ?exclude filter.')
        return queryset.exclude(id__in=exclude_ids)


class VariationTypeFilter(FilterSet):
    exclude = CharFilter(method='filter_exclude', label='Exclude Filter')

    class Meta:
        model = VariationType
        fields = '__all__'

    def filter_exclude(self, queryset, name, value):
        try:
            exclude_ids = [int(id) for id in value.split(',')]
        except Exception:
            raise APIException('Invalid values in ?exclude filter.')
        return queryset.exclude(id__in=exclude_ids)


class ProductVariationFilter(FilterSet):
    exclude = CharFilter(method='filter_exclude', label='Exclude Filter')

    class Meta:
        model = ProductVariation
        exclude = ('digital_file', 'thumbnail_image')

    def filter_exclude(self, queryset, name, value):
        try:
            exclude_ids = [int(id) for id in value.split(',')]
        except Exception:
            raise APIException('Invalid values in ?exclude filter.')
        return queryset.exclude(id__in=exclude_ids)
