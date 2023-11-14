from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from core.permissions import IsAdminOrReadOnly
from core.utils.permissions import IsOwnerOrAdmin
from core.utils.viewsets import DefaultViewSet
from oms.api.serializers.order import (OrderItemSerializer,
                                       OrderItemStatusSerializer,
                                       OrderSerializer, OrderStatusSerializer)
from oms.models.order import Order, OrderItemStatus, OrderStatus


class OrderAPI(DefaultViewSet):
    serializer_class = OrderSerializer
    search_fields = ['user_name', 'user_contact']
    queryset = Order.objects.filter().order_by('-id')
    permission_classes = [IsOwnerOrAdmin]

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            order = serializer.save()
            for order_items in request.data['order_items']:
                order_items['order'] = order.id
                serializer = OrderItemSerializer(data=order_items)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            order.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class OrderStatusAPI(DefaultViewSet):
    serializer_class = OrderStatusSerializer
    search_fields = ['name']
    queryset = OrderStatus.objects.filter().order_by('-id')
    permission_classes = [IsAdminOrReadOnly]


class OrderItemStatusAPI(DefaultViewSet):
    serializer_class = OrderItemStatusSerializer
    search_fields = ['name']
    queryset = OrderItemStatus.objects.filter().order_by('-id')
    permission_classes = [IsAdminOrReadOnly]
