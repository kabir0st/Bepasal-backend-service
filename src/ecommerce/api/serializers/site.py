from rest_framework import serializers


from ecommerce.models.ecom import QA, Cart, CartItem, Review, WishList
from oms.api.serializers.product import (
    ProductMiniSerializer, ProductVariationSerializer)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class QASerializer(serializers.ModelSerializer):
    class Meta:
        model = QA
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product_variation = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = '__all__'

    def get_product_variation(self, obj):
        return {
            **ProductMiniSerializer(obj.product_variation.product).data(),
            'selected_product': ProductVariationSerializer(
                obj.product_variation).data
        }


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'


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
