from django.urls import path

from speakerapi import consumers


ws_urlpatterns = [
    path('ws/speakerapi/init/checkauth/',
         consumers.WaitForAuthConsumer.as_asgi()),
    path('ws/speakerapi/incomingmessage/',
         consumers.IncomingMessageNotifyConsumer.as_asgi()),
    path('ws/speakerapi/measurements/',
         consumers.MeasurementNotifyConsumer.as_asgi()),
    path('ws/speakerapi/medicines/',
         consumers.MedicineNotifyConsumer.as_asgi()),
]
