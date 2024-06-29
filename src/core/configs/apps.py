COMMON_APPS = [
    'users',
    # lib
    'unfold',
    'unfold.contrib.filters',
    'rest_framework',
    'django_nextjs',
    'django_tenants',
    'drf_yasg',
    'django_filters',
    # defaults
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django_cleanup.apps.CleanupConfig'
]

TENANT_TYPES = {
    # public
    "public": {
        "APPS": ['tenants'] + COMMON_APPS,
        "URLCONF": "core.configs.urls.public"
    },
    "system": {
        "APPS": ['system'] + COMMON_APPS,
        "URLCONF": "core.configs.urls.system"
    },
    "ecommerce": {
        "APPS": ['system', 'ecommerce'] + COMMON_APPS,
        "URLCONF": "core.configs.urls.ecommerce"
    },
}
