from django_filters import FilterSet
from oms.models import Product
from oms.models.product import (
    Category, ProductVariation,
    VariationOption, VariationType
)


class ProductFilter(FilterSet):

    class Meta:
        model = Product
        exclude = ('thumbnail_image',)


class CategoryFilter(FilterSet):
    class Meta:
        model = Category
        fields = '__all__'


class VariationOptionFilter(FilterSet):
    class Meta:
        model = VariationOption
        fields = '__all__'


class VariationTypeFilter(FilterSet):
    class Meta:
        model = VariationType
        fields = '__all__'


class ProductVariationFilter(FilterSet):
    class Meta:
        model = ProductVariation
        exclude = ('digital_file', 'thumbnail_image')
