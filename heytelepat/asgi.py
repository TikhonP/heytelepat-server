"""
ASGI config for ***REMOVED*** project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import django

django.setup()

# noinspection PyPep8
from django.core.asgi import get_asgi_application
from speakerapi.routing import ws_urlpatterns as speakerapi_ws_urlpatterns
from staff.routing import ws_urlpatterns as staff_ws_urlpatterns
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(URLRouter(
        speakerapi_ws_urlpatterns + staff_ws_urlpatterns
    ))
})
