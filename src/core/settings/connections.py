import os

from .environments import DB_NAME, DB_PASSWORD, DB_USERNAME, channel

CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"

REDIS_URL = f"redis://127.0.0.1:6379/{channel}"
CELERY_BROKER_URL = REDIS_URL
CELERY_BROKER = REDIS_URL
SWAGGER_SETTINGS = {
    "DEFAULT_INFO": "app.urls.api_info",
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        'TIMEOUT': 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            'MAX_ENTRIES': 10000
        },
        'KEY_FUNCTION': 'django_tenants.cache.make_key',
        'REVERSE_KEY_FUNCTION': 'django_tenants.cache.reverse_key'
    }
}
CACHE_MIDDLEWARE_SECONDS = 60


DATABASES = {
    "default": {
        "ENGINE": "django_tenants.postgresql_backend",
        "NAME": DB_NAME,
        "USER": DB_USERNAME,
        "PASSWORD": DB_PASSWORD,
        "HOST": "127.0.0.1",
        "PORT": 5432,
    }
}

DATABASE_ROUTERS = ('django_tenants.routers.TenantSyncRouter', )
if os.environ.get("GITHUB_WORKFLOW"):
    DATABASES = {
        "default": {
            "ENGINE": "django_tenants.postgresql_backend",
            "NAME": "github_actions",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "127.0.0.1",
            "PORT": "5432",
        }
    }
