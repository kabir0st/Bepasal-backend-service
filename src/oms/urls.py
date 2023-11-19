from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from oms.api.items import (CategoryAPI, ItemAPI, ItemImageAPI,
                           ItemVariationAPI, VariationTypeAPI)
from oms.api.orders import OrderAPI, OrderItemStatusAPI, OrderStatusAPI

router = SimpleRouter()
router.register('categories', CategoryAPI)

router.register('items', ItemAPI)

router.register('status/order', OrderStatusAPI)
router.register('status/order-item', OrderItemStatusAPI)
router.register('orders', OrderAPI)
item_router = routers.NestedSimpleRouter(router,
                                         r'items',
                                         lookup='item')
item_router.register('images', ItemImageAPI)
item_router.register('variations', ItemVariationAPI)

router.register('variation-types', VariationTypeAPI)
variation_type_router = routers.NestedSimpleRouter(
    router, 'variation-types', lookup='id')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(item_router.urls)),
    path('', include(variation_type_router.urls))
]
