from django.urls import include, path
from rest_framework.routers import SimpleRouter
from tenants.logics import InstanceAPI

router = SimpleRouter()
router.register('', InstanceAPI)

urlpatterns = [path('', include(router.urls))]
