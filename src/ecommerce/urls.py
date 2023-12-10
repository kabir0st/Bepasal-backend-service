from django.urls import include, path
from rest_framework.routers import SimpleRouter

from ecommerce.api.site import (
    CartAPI, ReviewAPI, WishListAPI, get_product_related_info)

router = SimpleRouter()
router.register('reviews', ReviewAPI)
router.register('carts', CartAPI)
router.register('wishlist', WishListAPI)

urlpatterns = [
    path('product_info/<str:product_slug>/', get_product_related_info),
    path('', include(router.urls))
]
