import os

from .environments import (DB_NAME, DB_PASSWORD, DB_USERNAME, CHANNEL, DOCKER)

CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"

REDIS_HOST = '127.0.0.1'
DATABASE_HOST = '127.0.0.1'

if DOCKER:
    REDIS_HOST = 'redis'
    DATABASE_HOST = 'db'
REDIS_URL = f"redis://{REDIS_HOST}:6379/{CHANNEL}"

CELERY_BROKER_URL = REDIS_URL
CELERY_BROKER = REDIS_URL

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
DATABASE_HOST = "bepasal-db" if DOCKER else "127.0.0.1"

DATABASES = {
    "default": {
        "ENGINE": "django_tenants.postgresql_backend",
        "NAME": DB_NAME,
        "USER": DB_USERNAME,
        "PASSWORD": DB_PASSWORD,
        "HOST": DATABASE_HOST,
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
