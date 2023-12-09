from django.urls import include, path
from rest_framework.routers import SimpleRouter

from ecommerce.api.site import CartAPI, ReviewAPI

router = SimpleRouter()
router.register('reviews', ReviewAPI)
router.register('carts', CartAPI)

urlpatterns = [
    path('', include(router.urls))
]
