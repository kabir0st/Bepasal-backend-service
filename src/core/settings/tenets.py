import os

from core.settings.environments import BASE_DIR

TENANT_COLOR_ADMIN_APPS = True

STATICFILES_FINDERS = [
    "django_tenants.staticfiles.finders.TenantFileSystemFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

MULTITENANT_STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles/%s/"),
]

DEFAULT_FILE_STORAGE = "django_tenants.files.storage.TenantFileSystemStorage"

TENANT_MODEL = "tenants.Client"

TENANT_DOMAIN_MODEL = "tenants.Domain"

TENANT_SUBFOLDER_PREFIX = "bazar"

MULTI_TYPE_DATABASE_FIELD = 'type'

HAS_MULTI_TYPE_TENANTS = True

ROOT_URLCONF = ''

AUTH_USER_MODEL = "users.UserBase"
