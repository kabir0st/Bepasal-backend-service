from rest_framework import serializers


from ecommerce.models.ecom import QA, Cart, Review
from oms.api.serializers.product import (
    ProductListSerializer, ProductVariationSerializer)


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
        model = Review
        fields = '__all__'

    def get_product_variation(self, obj):
        return {
            **ProductListSerializer(obj.product_variation.product).data(),
            'selected_product': ProductVariationSerializer(
                obj.product_variation).data
        }


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'
