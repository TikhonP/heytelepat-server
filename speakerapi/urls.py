from django.urls import path

from speakerapi import views

urlpatterns = [
    path('speaker/', views.SpeakerAPIView.as_view(), name='speakerapi-speaker'),
    path('speaker/init/', views.InitSpeakerAPIView.as_view(), name='speakerapi-speaker-init'),
    path('message/', views.IncomingMessageNotifyApiView.as_view(), name='speakerapi-message-list'),
    path('message/send/', views.SendMessageApiView.as_view(), name='speakerapi-message-send'),
    path('measurement/', views.MeasurementListAPIView.as_view(), name='speakerapi-measurement'),
    path('measurement/categories/', views.GetListOfAllCategories.as_view(),
         name='speakerapi-measurement-categories-list'),
    path('measurement/push/', views.SendValueAPIView.as_view(), name='speakerapi-measurement-push'),
    path('measurement/call/push/', views.SendValueFromCallAPIView.as_view(), name='speakerapi-measurement-call-push'),
    path('medicine/', views.MedicineListAPIView.as_view(), name='speakerapi-medicine'),
    path('medicine/commit/', views.CommitMedicineApiView.as_view(), name='speakerapi-medicine-commit'),
    path('firmware/', views.CheckFirmwareAPIView.as_view(), name='speakerapi-firmware'),
    path('exception/', views.SpeakerExceptionAPIView.as_view(), name='speakerapi-exception'),
]
