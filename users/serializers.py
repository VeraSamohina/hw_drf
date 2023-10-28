from rest_framework import serializers

from payments.models import Payment
from payments.serializers import PaymentSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(source='payment_set', many=True)

    class Meta:
        model = User
        fields = ('email', 'phone', 'city', 'payments')
