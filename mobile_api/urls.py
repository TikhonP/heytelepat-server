from django.urls import path

from mobile_api import views

urlpatterns = [
    path('speaker/', views.CreateNewSpeakerAPIView.as_view(), name='mobile-api-speaker'),
]
