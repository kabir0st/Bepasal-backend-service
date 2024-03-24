from django.conf import settings as django_setting
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users.api.auth import login, login_refresh, logout, whoami
from users.api.support_app import DocumentAPI, VerificationCodeAPI

router = SimpleRouter()
router.register('verifications', VerificationCodeAPI)

router.register('documents', DocumentAPI)

urlpatterns = [
    path('api/app/auth/refresh/', login_refresh),
    path('api/app/auth/logout/', logout),
    path('api/app/auth/', login),
    path('api/app/whoami/', whoami),
    path('api/users/', include('users.urls')),
]
urlpatterns += static(django_setting.MEDIA_URL,
                      document_root=django_setting.MEDIA_ROOT)
urlpatterns += static(django_setting.STATIC_URL,
                      document_root=django_setting.STATIC_ROOT)
urlpatterns += [path('', admin.site.urls)]
