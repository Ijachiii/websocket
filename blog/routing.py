from django.urls import re_path
from . import consumers
import os

from django.core.asgi import get_asgi_application

websocket_urlpatterns = [
    re_path(r'ws/blog/(?P<blog_id>\w+)/$', consumers.CommentConsumer.as_asgi()),
]

# (?P<blog_id>\d+)/comments/$"
