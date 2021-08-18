from django.urls import path

from medsenger_agent import views

urlpatterns = [
    path('init', views.InitAPIView.as_view()),
    path('remove', views.RemoveContractAPIView.as_view()),
    path('status', views.StatusAPIView.as_view()),
    path('settings', views.settings),
    path('message', views.IncomingMessageApiView.as_view()),
    path('newdevice', views.newdevice, name='medsenger-newdevice'),
    path('order', views.OrderApiView.as_view()),
]
