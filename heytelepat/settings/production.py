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
