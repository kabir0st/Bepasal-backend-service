from decimal import Decimal

from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from core.permissions import IsStaffOrReadOnly
from core.utils.permissions import IsOwnerOrAdmin
from core.utils.viewsets import DefaultViewSet
from oms.api.serializers.order import (OrderItemSerializer,
                                       OrderItemStatusSerializer,
                                       OrderSerializer, OrderStatusSerializer)
from oms.api.serializers.payments import PaymentSerializer
from oms.models import Payment
from oms.models.order import Order, OrderItemStatus, OrderStatus
from oms.models.payment import FonePayPayment
from oms.utils import generate_fonepay_qr, verify_qr


class OrderAPI(DefaultViewSet):
    serializer_class = OrderSerializer
    search_fields = ['user_name', 'user_contact']
    queryset = Order.objects.filter().order_by('-id')
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(user=self.user)

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

    @action(methods=['POST', 'post'], detail=True)
    def staff_approved_payment(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise APIException('Only Staff can add staff approved payments.')
        summary = self.get_object()
        with transaction.atomic():
            Payment.objects.create(payment_type='staff_approved',
                                   amount=Decimal(f'{request.data["amount"]}'),
                                   invoice_summary=summary,
                                   remarks='Payment Through API')
            response = {
                'status': True,
                'data': OrderSerializer(summary).data,
                'type': 'invoice-summary'
            }
        return Response(response, status=status.HTTP_202_ACCEPTED)

    @action(methods=['post'], detail=True)
    def initiate_fonepay(self, request, *args, **kwargs):
        obj = self.get_object()
        fonepay_obj = FonePayPayment.objects.create(
            amount=request.data['amount'], invoice_number=obj.invoice_number)
        res = generate_fonepay_qr(fonepay_obj)
        return Response(res)

    @action(methods=['post'], detail=True)
    def verify_fonepay(self, request, *args, **kwargs):
        obj = FonePayPayment.objects.get(id=request.data['fonepay_payment_id'])
        obj.qr_status = 'success'
        obj.save()
        if obj.is_verified_from_server:
            raise Exception('Cannot verify payments that is already verified')
        with transaction.atomic():
            res = verify_qr(obj)
            if res['status']:
                payment_data = {
                    'amount': obj.amount,
                    'fonepay_payment': obj.id,
                    'payment_type': 'fonepay',
                    'invoice_summary': self.get_object().id
                }
                serializer = PaymentSerializer(data=payment_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({
                    'status': True,
                    'msg': 'Payment successful.',
                    'data-type': 'payment',
                    'data': serializer.data
                })
            return Response({
                'status': False,
                'msg': 'There was problem verifying your payment.',
                'exception': res['text']
            })


class OrderStatusAPI(DefaultViewSet):
    serializer_class = OrderStatusSerializer
    search_fields = ['name']
    queryset = OrderStatus.objects.filter().order_by('-id')
    permission_classes = [IsStaffOrReadOnly]


class OrderItemStatusAPI(DefaultViewSet):
    serializer_class = OrderItemStatusSerializer
    search_fields = ['name']
    queryset = OrderItemStatus.objects.filter().order_by('-id')
    permission_classes = [IsStaffOrReadOnly]
