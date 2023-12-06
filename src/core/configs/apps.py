COMMON_APPS = [
    'users',
    # lib
    'rest_framework',
    'django_nextjs',
    'django_tenants',
    'drf_yasg',
    'django_filters',
    'ckeditor',
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
    "oms": {
        "APPS": ['oms'] + COMMON_APPS,
        "URLCONF": "core.configs.urls.oms"
    },
    "ecommerce": {
        "APPS": ['oms', 'ecommerce'] + COMMON_APPS,
        "URLCONF": "core.configs.urls.ecommerce"
    },
}
