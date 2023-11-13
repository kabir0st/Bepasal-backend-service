from rest_framework import serializers

from oms.models.order import Order, OrderItem
from .item import ItemVariationSerializer, ItemSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    item_detail = ItemSerializer(source='item', read_only=True)
    variation_detail = ItemVariationSerializer(
        source='variation', read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(
        many=True, source='order_items', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
