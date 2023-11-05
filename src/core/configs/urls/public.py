from django.conf import settings as django_setting
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

urlpatterns = [
    # path('api/instances/', include('tenant.urls')),
    path('super/', admin.site.urls),
]
urlpatterns += static(django_setting.MEDIA_URL,
                      document_root=django_setting.MEDIA_ROOT)
urlpatterns += static(django_setting.STATIC_URL,
                      document_root=django_setting.STATIC_ROOT)
