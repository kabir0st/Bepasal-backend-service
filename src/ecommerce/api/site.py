
from django.db import transaction
from requests import Response
from rest_framework import status
from rest_framework.decorators import action

from core.utils.permissions import IsOwnerOrAdmin, IsOwnerOrReadOnly
from core.utils.viewsets import DefaultViewSet
from ecommerce.api.serializers.site import CartSerializer, ReviewSerializer
from ecommerce.models.ecom import Cart, CartItem, Review
from oms.models.product import ProductVariation


class CartAPI(DefaultViewSet):
    serializer_class = CartSerializer
    search_fields = ['user']
    queryset = Cart.objects.filter().order_by('-id')
    permission_classes = [IsOwnerOrAdmin]

    @action(methods=['POST'], detail=True, )
    def add_to_cart(self, request, *args, **kwargs):
        obj = self.get_object()
        with transaction.atomic():
            for item in request.data['items']:
                product = ProductVariation.objects.get(id=item)
                cart_item, _ = CartItem.objects.get_or_create(
                    cart=obj, product_variation=product)
                cart_item.quantity = item['quantity']
                cart_item.save()
        # to trigger updated_at
        obj.save()
        return Response({'status': True, 'msg': "Item added to cart."},
                        status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=True)
    def remove_product_from_cart(self, request, *args, **kwargs):
        obj = self.get_object()
        with transaction.atomic():
            for item in request.data['items']:
                product = ProductVariation.objects.get(id=item)
                cart_item = CartItem.objects.get(
                    cart=obj, product_variation=product)
                cart_item.delete()
        # to trigger updated_at
        obj.save()
        return Response({'status': True, 'msg': "Item added to cart."},
                        status=status.HTTP_201_CREATED)


class ReviewAPI(DefaultViewSet):
    '''
    ?product=__id__ is needed if no user is logged in.
    '''
    serializer_class = ReviewSerializer
    search_fields = ['user', 'product__name']
    queryset = Review.objects.filter().order_by('-id')
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        product_id = self.request.GET.get('product', None)
        if self.request.user.is_authenticated():
            if self.request.user.is_staff:
                return self.queryset
            if not product_id:
                return self.queryset.filter(user=self.request.user)
        if product_id:
            return self.queryset.filter(product__id=product_id)
        return self.queryset.none()
