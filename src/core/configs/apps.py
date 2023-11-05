
TENANT_TYPES = {
    # public
    "public": {
        "APPS": [
            'users',
            'django_tenants',
            "tenants",
            # lib
            'rest_framework',
            # defaults
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
        ],
        "URLCONF": "core.configs.urls.public"
    },
    # "portfolio": {
    #     "APPS": [
    #         'users',
    #         "cms",
    #         # lib
    #         'rest_framework',
    #         # defaults
    #         'django.contrib.admin',
    #         'django.contrib.auth',
    #         'django.contrib.contenttypes',
    #         'django.contrib.sessions',
    #         'django.contrib.messages',
    #         'django.contrib.staticfiles',
    #     ],
    #     "URLCONF": "core.configs.urls.portfolio"
    # },
    # "oms": {
    #     "APPS": ['users',
    #              "cms",
    #              # lib
    #              'rest_framework',
    #              # defaults
    #              'django.contrib.admin',
    #              'django.contrib.auth',
    #              'django.contrib.contenttypes',
    #              'django.contrib.sessions',
    #              'django.contrib.messages',
    #              'django.contrib.staticfiles',],
    #     "URLCONF": "core.configs.urls.oms"
    # },
}
