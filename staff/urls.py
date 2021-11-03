from django.urls import path

from staff import views

urlpatterns = [
    path('issue/add/', views.create_issue, name='add-issue'),
    path('issue/log/<int:issue_id>/<str:speaker_token>/', views.receive_file),
]
