from django.urls import path , include
from Wall.consumers import ChatConsumer


websocket_urlpatterns = [
    path("" , ChatConsumer.as_asgi()) , 
]