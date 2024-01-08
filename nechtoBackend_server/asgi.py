"""
ASGI config for nechtoBackend_server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from nechtoBackend_server.wsurls import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nechtoBackend_server.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(websocket_urlpatterns),
})
