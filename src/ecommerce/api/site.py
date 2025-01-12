
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.utils.permissions import IsOwnerOrAdmin, IsOwnerOrReadOnly
from core.utils.viewsets import DefaultViewSet
from ecommerce.api.serializers.site import (CartSerializer, QASerializer,
                                            ReviewSerializer,
                                            WishListSerializer)
from ecommerce.models.ecom import QA, Cart, Review, WishList
from system.models.product import ProductVariation


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
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return self.queryset
            if not product_id:
                return self.queryset.filter(user=self.request.user)
        if product_id:
            print(product_id)
            return self.queryset.filter(product__id=product_id)
        return self.queryset.none()


def get_initial_load(product_slug):
    reviews = Review.objects.filter(
        product__slug=product_slug).order_by('-id')[:5]
    qas = QA.objects.filter(
        product__slug=product_slug).order_by('-id')[:5]
    return {
        'reviews': ReviewSerializer(reviews, many=True).data,
        'qas': QASerializer(qas, many=True).data
    }


@api_view(['GET'])
def get_product_related_info(request, product_slug):
    return Response(get_initial_load(product_slug),
                    status=status.HTTP_200_OK)


class CartAPI(GenericViewSet):
    serializer_class = CartSerializer
    search_fields = ['user']
    queryset = Cart.objects.filter().order_by('-id')
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='add-to-cart')
    def add_to_cart(self, request):
        user = self.request.user
        with transaction.atomic():
            cart, _ = Cart.objects.get_or_create(user=user)
            product_variation_slug = request.data.get('product_variation_slug')
            product_variation = ProductVariation.objects.get(
                slug=product_variation_slug)
            cart.product_variations.add(product_variation.id)
            cart.quantities[product_variation.slug] = request.data.get(
                'quantity', 1)
            cart.save()
        return Response({'status': True}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='remove-from-cart')
    def remove_from_cart(self, request):
        user = self.request.user
        try:
            wishlist = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({'detail': 'Wishlist does not exist'},
                            status=status.HTTP_404_NOT_FOUND)
        product_variation_slug = request.data.get('product_variation_slug')
        product_variation = ProductVariation.objects.get(
            slug=product_variation_slug)
        wishlist.product_variations.remove(product_variation.id)
        wishlist.quantities.pop(product_variation.slug)
        wishlist.save()
        return Response({'status': True}, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class WishListAPI(GenericViewSet):
    serializer_class = WishListSerializer
    queryset = WishList.objects.filter().order_by('-id')
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        if not self.request.user.is_staff:
            return self.queryset.filter(user=self.request.user)
        return super().get_queryset()

    @action(detail=False, methods=['post'], url_path='add-to-wishlist')
    def add_to_wishlist(self, request):
        with transaction.atomic():
            user = self.request.user
            wishlist, _ = WishList.objects.get_or_create(user=user)
            product_variation_slug = request.data.get('product_variation_slug')
            product_variation = ProductVariation.objects.get(
                slug=product_variation_slug)
            wishlist.product_variations.add(product_variation.id)
            wishlist.save()
        return Response({'status': True}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='remove-from-wishlist')
    def remove_from_wishlist(self, request):
        user = self.request.user
        try:
            wishlist = WishList.objects.get(user=user)
        except WishList.DoesNotExist:
            return Response({'detail': 'Wishlist does not exist'},
                            status=status.HTTP_404_NOT_FOUND)
        product_variation_slug = request.data.get('product_variation_slug')
        product_variation = ProductVariation.objects.get(
            slug=product_variation_slug)
        wishlist.product_variations.remove(product_variation.id)
        wishlist.save()
        return Response({'status': True}, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
