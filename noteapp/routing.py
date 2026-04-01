from django.urls import path,re_path
from .consumers import DocumentListConsumer


ws_urlspatterns = [
    re_path(r'ws/documents/$', DocumentListConsumer.as_asgi()),
]