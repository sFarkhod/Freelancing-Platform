from django.urls import path
from user.consumers import NotificationConsumer


websocket_urlpatterns = [
    path(r'ws/notifications/', NotificationConsumer.as_asgi()),
]