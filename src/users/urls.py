from django.urls import include, path
from rest_framework.routers import SimpleRouter
from users.api.users import RegisterUserBaseAPI, UserBaseAPI
from users.api.settings import SettingsAPI
from users.api.auth import verify_email_address

router = SimpleRouter()

router.register('settings', SettingsAPI)
router.register('', UserBaseAPI, basename='Users')

urlpatterns = [
    path('register/', RegisterUserBaseAPI.as_view()),
    path('verify/', verify_email_address),
    path('', include(router.urls)),
]
