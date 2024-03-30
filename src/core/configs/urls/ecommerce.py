from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .base_url import urlpatterns

# urlpatterns += [path("", include("django_nextjs.urls"))]
# urlpatterns.append(re_path(r'^(?:.*)/?$', index))
