from rest_framework import serializers


from ecommerce.models.ecom import QA, Cart,  Review, WishList
from system.api.serializers.product import (
    ProductMiniSerializer, ProductVariationSerializer)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class QASerializer(serializers.ModelSerializer):
    class Meta:
        model = QA
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    product_variations = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = '__all__'

    def get_product_variations(self, obj):
        return [
            {
                **ProductMiniSerializer(item.product).data,
                'selected_product': ProductVariationSerializer(
                    item).data
            } for item in obj.product_variations.all()
        ]


class WishListSerializer(serializers.ModelSerializer):
    product_variations_details = serializers.SerializerMethodField()

    class Meta:
        model = WishList
        fields = '__all__'

    def get_product_variations_details(self, obj):
        return [
            {
                **ProductMiniSerializer(item.product).data,
                'selected_product': ProductVariationSerializer(
                    item).data
            } for item in obj.product_variations.all()
        ]
