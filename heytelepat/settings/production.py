from .base import *


DEBUG = False

ALLOWED_HOSTS = [
    '194.87.234.236',
]

DOMEN = 'http://194.87.234.236'

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
        'NAME': 'heytelepat',
        'USER': 'heytelepatuser',
        'PASSWORD': 'As3IU82rj2GJKj9b_NWPYw',
        'HOST': 'localhost',
        'PORT': '',
    }
}
