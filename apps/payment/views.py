from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from apps.booking.models import Booking
from apps.booking.permissions import IsParent
from apps.payment import serializers
from apps.payment.models import Payment
from apps.payment.serializers import PaymentSerializer
from django.db import IntegrityError

# Create your views here.
class ListPaymentDetailView(generics.ListAPIView):
    serializer_class = serializers.ListPaymentSerializer
    permission_classes = [IsParent, ]

    def get_object(self):
        booking = Booking.objects.filter(pk=self.kwargs.get('booking_id')).first()
        if booking:
            return booking
        else:
            raise ValidationError({'error': 'No any booking available for following id '})

    def get_queryset(self):
        instance = self.get_object()
        return Booking.objects.filter(
            nanny=instance.nanny,
            status='accepted',
            has_paid=False,
            parent=self.request.user
        )


class CreatePaymentView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsParent, ]

    def get_object(self):
        booking = Booking.objects.filter(pk=self.kwargs.get('booking_id')).first()
        if booking:
            return booking
        else:
            raise ValidationError({'error': 'No any booking available for following id '})

    def perform_create(self, serializer):
        instance = self.get_object()
        if serializer.validated_data.get('amount') != instance.total_amount:
            raise ValidationError({
                'error': 'Amount did not match'
            })
        try:

            Payment.objects.create(
                booking=instance,
                amount=serializer.validated_data.get('amount'),
                to_be_paid_by=self.request.user,
                status='completed'
            )
            instance.has_paid = True
            instance.save()
        except IntegrityError:
            raise ValidationError({
                'error':'error payment already exists'
            })
