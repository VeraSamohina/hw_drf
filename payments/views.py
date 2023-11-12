import os

import stripe
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course
from payments.models import Payment
from payments.serializers import PaymentSerializer
from payments.services import create_payment_intent


class PaymentListAPIView(generics.ListAPIView):
    """ Представления списка платежей"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['date']
    filterset_fields = ('lesson', 'course', 'payment_type')


class PaymentCreateAPIView(generics.CreateAPIView):
    """
    Создание платежа

    create:
    создает платеж в системе stripe и в БД
    """

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        course = Course.objects.get(id=kwargs.get('pk'))
        payment_intent = create_payment_intent(kwargs.get('pk'))
        user = self.request.user
        payment_id = payment_intent.id
        # Формирование данных для сохранения в объект класса Payment
        data = {
            'stripe_id': payment_id,
            'amount': course.price,
            'payment_type': 'TRANSFER_TO_ACCOUNT',
            'user': user.id,
            'course': course.id,
            'is_confirmed': True
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status= status.HTTP_201_CREATED, headers=headers
        )


class GetPaymentView(APIView):
    """
    Получение информации о платеже.

    get:
    Получает информацию о платеже по его ID.
    """

    def get(self, request, payment_id):
        payment_intent = stripe.PaymentIntent.retrieve(payment_id)
        return Response({
            'status': payment_intent.status, })
