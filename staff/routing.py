from django.urls import path

from staff import consumers

ws_urlpatterns = [
    path('ws/staff/issue/', consumers.IssuesConsumer.as_asgi()),
]
