from rest_framework import serializers

from oms.models.order import (Order, OrderItem, OrderItemStatus, OrderStatus)
from .item import ItemVariationSerializer, ItemSerializer


class OrderStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderStatus
        fields = '__all__'


class OrderItemStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItemStatus
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    item_detail = ItemSerializer(source='item', read_only=True)
    variation_detail = ItemVariationSerializer(
        source='variation', read_only=True)
    status_detail = OrderItemStatusSerializer(source='status', read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_item_details = OrderItemSerializer(
        many=True, source='order_items', read_only=True)
    status_detail = OrderStatusSerializer(source='status', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
