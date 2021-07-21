from django.urls import path
from speakerapi import views

urlpatterns = [
    path('init/', views.SpeakerInitApiView.as_view()),
    path('remove/', views.SpeakerDeleteApiView.as_view()),
    path('sendmessage/', views.SendMessageApiView.as_view()),
    path('pushvalue/', views.SendValueApiView.as_view()),
    path('incomingmessage/', views.IncomingMessageNotifyApiView.as_view()),
    path('getlistcategories/', views.GetListOfAllCategories.as_view()),
    path('measurements/', views.MeasurementListAPIView.as_view()),
    path('medicine/commit/', views.CommitMedicineApiView.as_view()),
    path('medicine/', views.MedicineListAPIView.as_view()),
]
