from rest_framework import serializers

from core.utils.serializers import Base64ImageField
from oms.models.item import (Category, Item, ItemImage, ItemVariation,
                             ItemVariationImage, VariationType)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ItemImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = ItemImage
        fields = '__all__'


class VariationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariationType
        fields = '__all__'


class ItemVariationImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = ItemVariationImage
        fields = '__all__'


class ItemVariationSerializer(serializers.ModelSerializer):
    images = ItemVariationImageSerializer(many=True)

    class Meta:
        model = ItemVariation
        fields = '__all__'


class ItemListSerializer(serializers.ModelSerializer):

    # category_str = serializers.CharField(source='category.name')

    class Meta:
        model = Item
        fields = ('name',  'thumbnail_image', 'slug',
                  'selling_price',
                  'crossed_price', 'quantity', 'sku')


class ItemSerializer(serializers.ModelSerializer):
    images = ItemImageSerializer(many=True, read_only=True)
    thumbnail_image = Base64ImageField()
    variations = ItemVariationSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        exclude = ('cost_price',)
