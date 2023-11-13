from django.urls import path

from payments.apps import PaymentsConfig
from payments.views import PaymentListAPIView, PaymentCreateAPIView, GetPaymentView

app_name = PaymentsConfig.name

urlpatterns = [
    path('', PaymentListAPIView.as_view()),
    path('create/<int:pk>/', PaymentCreateAPIView.as_view(), name='payment_create'),
    path('<str:payment_id>/', GetPaymentView.as_view(), name='payment_get'),
]
