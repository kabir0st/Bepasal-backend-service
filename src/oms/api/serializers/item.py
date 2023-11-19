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

    variation_type_name = serializers.CharField(source='variation_type.name')

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
    images = ItemVariationImageSerializer(many=True, read_only=True)
    variation_option_combination_detail = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = ItemVariation
        fields = '__all__'

    def get_images(self, instance):
        return ItemVariationImageSerializer(
            instance.images.filter(), many=True).data

    def get_variation_option_combination_detail(self, instance):
        return VariationOptionSerializer(
            instance.variation_option_combination.filter(), many=True).data

    def to_representation(self, instance):
        request = self.context.get('request')
        is_admin = request.user.is_staff if request else False
        representation = super(
            ItemVariationSerializer, self).to_representation(instance)
        if not is_admin:
            representation.pop('cost_price', None)
        return representation


class ItemListSerializer(serializers.ModelSerializer):
    category_details = serializers.SerializerMethodField(read_only=True)
    default_variation = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Item
        fields = "__all__"

    def get_category_details(self, instance):
        return CategorySerializer(instance.catagories, many=True).data

    def get_default_variation(self, instance):
        return ItemVariationSerializer(
            instance.variations.filter(
                is_active=True, is_default_variation=True).order_by(
                    '-id').first(), context={'request': self.context.get(
                        'request')}).data


class ItemSerializer(ItemListSerializer):
    category_details = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    variations = serializers.SerializerMethodField(read_only=True)
    thumbnail_image = Base64ImageField(required=False)  # Make it optional

    class Meta:
        model = Item
        fields = '__all__'

    def get_images(self, instance):
        return ItemImageSerializer(instance.images.filter(), many=True).data

    def get_variations(self, instance):
        return ItemVariationSerializer(
            instance.variations.filter(is_active=True),
            many=True, context={'request': self.context.get('request')}).data
