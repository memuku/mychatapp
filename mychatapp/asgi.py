import os

from django.core.asgi import get_asgi_application

# Import the channels libraries
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_app_django.settings')

# Set up the application with both HTTP and WebSocket handling
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handles HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns  # Handles WebSocket requests
        )
    ),
})
