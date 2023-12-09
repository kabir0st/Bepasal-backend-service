from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from core.utils.logics import index
from .base_url import urlpatterns

SchemaView = get_schema_view(
    openapi.Info(
        title="BePasal API",
        default_version='v1',
        description="",
        terms_of_service="",
        contact=openapi.Contact(email="himalayancreatives.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    urlconf='',
    patterns=[*urlpatterns],
    permission_classes=[permissions.AllowAny],
)


urlpatterns += [
    path('api/system/', include('oms.urls')),
]
urlpatterns += [path("api/docs/",
                     SchemaView.with_ui('swagger', cache_timeout=0),
                     name='schema-swagger-ui')]
urlpatterns += [path("", include("django_nextjs.urls"))]
urlpatterns.append(re_path(r'^(?:.*)/?$', index))
