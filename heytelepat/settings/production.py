from .base import *


DEBUG = False

ALLOWED_HOSTS = [
    '194.87.234.236',
]

DOMAIN = 'http://194.87.234.236'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '***REMOVED***',
        'USER': '***REMOVED***user',
        'PASSWORD': '***REMOVED***',
        'HOST': 'localhost',
        'PORT': '',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ]
}
