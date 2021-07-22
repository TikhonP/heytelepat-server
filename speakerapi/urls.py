from django.urls import path

from speakerapi import views

urlpatterns = [
    path('speaker/', views.SpeakerAPIView.as_view(), name='speakerapi-speaker'),
    path('message/', views.IncomingMessageNotifyApiView.as_view(), name='speakerapi-message-list'),
    path('message/send/', views.SendMessageApiView.as_view(), name='speakerapi-message-send'),
    path('measurement/', views.MeasurementListAPIView.as_view(), name='speakerapi-measurement'),
    path('measurement/categories/', views.GetListOfAllCategories.as_view(),
         name='speakerapi-measurement-categories-list'),
    path('measurement/push/', views.SendValueAPIView.as_view(), name='speakerapi-measurement-push'),
    path('medicine/', views.MedicineListAPIView.as_view(), name='speakerapi-medicine'),
    path('medicine/commit/', views.CommitMedicineApiView.as_view(), name='speakerapi-medicine-commit'),
    path('firmware/', views.CheckFirmwareAPIView.as_view(), name='speakerapi-firmware'),
]
