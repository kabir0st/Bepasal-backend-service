from rest_framework import serializers

from core.utils.serializers import Base64ImageField
from oms.models.product import (Category, Product, ProductImage,
                                ProductVariation,
                                ProductVariationImage, VariationOption,
                                VariationType)
from django.db.models import Sum


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = ProductImage
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


class ProductVariationImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = ProductVariationImage
        fields = '__all__'


class ProductVariationSerializer(serializers.ModelSerializer):
    images = ProductVariationImageSerializer(many=True, read_only=True)
    variation_option_combination_detail = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = ProductVariation
        fields = '__all__'

    def get_images(self, instance):
        return ProductVariationImageSerializer(
            instance.images.filter(), many=True).data

    def get_variation_option_combination_detail(self, instance):
        return VariationOptionSerializer(
            instance.variation_option_combination.filter(), many=True).data

    def to_representation(self, instance):
        request = self.context.get('request')
        is_admin = request.user.is_staff if request else False
        representation = super(
            ProductVariationSerializer, self).to_representation(instance)
        if not is_admin:
            representation.pop('cost_price', None)
            representation.pop('digital_file', None)
        return representation


class ProductListSerializer(serializers.ModelSerializer):
    category_details = serializers.SerializerMethodField(read_only=True)
    default_variation = serializers.SerializerMethodField(read_only=True)
    test_thumbnail_image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

    def get_test_thumbnail_image(self, instance):
        return 'https://picsum.photos/500'

    def get_category_details(self, instance):
        return CategorySerializer(instance.categories, many=True).data

    def get_default_variation(self, instance):
        if default_var := instance.variations.filter(
                is_active=True, is_default_variation=True).first():
            return ProductVariationSerializer(
                default_var, context={'request': self.context.get(
                    'request')}).data
        return ProductVariationSerializer(
            instance.variations.filter(
                is_active=True).first(), context={'request': self.context.get(
                    'request')}).data


class AdminProductListSerializer(serializers.ModelSerializer):
    total_stock = serializers.SerializerMethodField(read_only=True)
    total_sold = serializers.SerializerMethodField(read_only=True)
    highest_cost_price = serializers.SerializerMethodField(read_only=True)
    highest_selling_price = serializers.SerializerMethodField(read_only=True)
    enabled_variations = serializers.SerializerMethodField(read_only=True)
    variants = serializers.SerializerMethodField(read_only=True)
    test_thumbnail_image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

    def get_test_thumbnail_image(self, instance):
        return 'https://picsum.photos/500'

    def get_total_sold(self, instance):
        total_sold = 0
        for variation in instance.variations.all():
            sold = variation.order_items.filter(
                is_cancelled=False).aggregate(
                    total_sold=Sum('quantity'))['total_sold']
            total_sold += sold if sold is not None else 0
        return total_sold

    def get_highest_cost_price(self, instance):
        price = instance.variations.order_by('-cost_price').first().cost_price
        return f"Rs. {price}/-"

    def get_highest_selling_price(self, instance):
        price = instance.variations.order_by(
            '-selling_price').first().selling_price
        return f"Rs. {price}/-"

    def get_total_stock(self, instance):
        total_stock = instance.variations.filter(
        ).aggregate(
            total_stock=Sum('stock'))['total_stock']
        return total_stock if total_stock is not None else 0

    def get_enabled_variations(self, instance):
        return ", ".join([
            variation.name for variation in
            instance.enabled_variation_types.filter(
            )
        ])

    def get_variants(self, instance):
        return instance.variations.count()


class ProductSerializer(ProductListSerializer):
    category_details = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    variations = serializers.SerializerMethodField(read_only=True)
    thumbnail_image = Base64ImageField(required=False)

    class Meta:
        model = Product
        fields = '__all__'

    def get_images(self, instance):
        return ProductImageSerializer(instance.images.filter(), many=True).data

    def get_variations(self, instance):
        return ProductVariationSerializer(
            instance.variations.filter(is_active=True),
            many=True, context={'request': self.context.get('request')}).data
