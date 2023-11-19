from rest_framework import serializers

from apps.booking.models import Booking
from apps.common.choices import PaymentChoices
from apps.payment.models import PaymentMethod


class ListPaymentSerializer(serializers.ModelSerializer):
    nanny_name = serializers.CharField(source='nanny.fullname', read_only=True)
    job_commitment = serializers.CharField(source='commitment.name')
    start_date = serializers.CharField(source='get_start_date')
    days_worked = serializers.IntegerField(source='calculate_days_worked')
    hours_worked = serializers.CharField(source='calculate_total_hours_worked')
    hourly_rate = serializers.FloatField(source='nanny.amount_per_hour')
    total_amount = serializers.FloatField()

    class Meta:
        model = Booking
        fields = [
            'nanny_name',
            'job_commitment',
            'start_date',
            'days_worked',
            'hours_worked',
            'has_paid',
            'hourly_rate',
            'total_amount',
        ]


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = [
            'method',
            'image',
            'payment_method'
        ]


class PaymentSerializer(serializers.Serializer):
    amount = serializers.FloatField()
    method = serializers.ChoiceField(choices=PaymentChoices.choices)