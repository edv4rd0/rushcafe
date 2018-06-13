from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack

import rushcafe.routing

application = ProtocolTypeRouter({
    'websocket': SessionMiddlewareStack(
        URLRouter(
            rushcafe.routing.websocket_urlpatterns
        ),
    ),
})
