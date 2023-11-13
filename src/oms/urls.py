from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from oms.api.items import (CategoryAPI, ItemAPI, ItemImageAPI,
                           ItemVariationAPI, VariationTypeAPI)
from oms.api.orders import OrderAPI

router = SimpleRouter()
router.register('categories', CategoryAPI)

router.register('items', ItemAPI)
router.register('orders', OrderAPI)

item_router = routers.NestedSimpleRouter(router,
                                         r'items',
                                         lookup='item')
item_router.register('images', ItemImageAPI)
item_router.register('variation_types', VariationTypeAPI)
item_router.register('variations', ItemVariationAPI)

urlpatterns = [
    path('', include(router.urls)),
]
