from rest_framework import serializers

from core.utils.serializers import Base64ImageField
from oms.models.item import (Category, Item, ItemImage, ItemVariation,
                             ItemVariationImage, VariationOption,
                             VariationType)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ItemImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = ItemImage
        fields = '__all__'


class VariationOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariationOption
        fields = '__all__'


class VariationTypeSerializer(serializers.ModelSerializer):

    variation_options = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = VariationType
        fields = '__all__'

    def get_variation_options(self, instance):
        return VariationOptionSerializer(
            instance.options.filter(), many=True).data


class ItemVariationImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = ItemVariationImage
        fields = '__all__'


class ItemVariationSerializer(serializers.ModelSerializer):
    images = ItemVariationImageSerializer(many=True)
    variation_option_combination_detail = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = ItemVariation
        fields = '__all__'

    def get_variation_option_combination_detail(self, instance):
        return VariationOptionSerializer(
            instance.variation_option_combination.filter(), many=True).data


class ItemListSerializer(serializers.ModelSerializer):
    category_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Item
        fields = ('name',  'thumbnail_image', 'slug',
                  'selling_price',
                  'crossed_price', 'quantity', 'sku', 'is_active',
                  'category_details')

    def get_category_details(self, instance):
        return CategorySerializer(instance.category).data


class ItemSerializer(serializers.ModelSerializer):
    images = ItemImageSerializer(many=True, read_only=True)
    thumbnail_image = Base64ImageField()
    variations = ItemVariationSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        exclude = ('cost_price',)
