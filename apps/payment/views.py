from django.db import IntegrityError
from rest_framework import generics
from rest_framework.exceptions import ValidationError

from apps.booking.models import Booking
from apps.booking.permissions import IsParent, IsNanny
from apps.notification.models import Notification
from apps.payment import serializers
from apps.payment.models import Payment, PaymentMethod
from apps.payment.serializers import PaymentSerializer, PaymentMethodSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

from apps.users.models import Device
import requests


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
                'error': 'error payment already exists'
            })


class PaymentMethodView(generics.ListAPIView):
    serializer_class = PaymentMethodSerializer

    def get_queryset(self):
        return PaymentMethod.objects.all()


class RequestForPaymentView(APIView):
    permission_classes = [IsNanny]

    def post(self, request, *args, **kwargs):
        kwargs = kwargs.get('booking_id')
        print(kwargs)
        booking = Booking.objects.filter(pk=kwargs).first()

        if booking:
            if booking.status == 'accepted':
                parent_device = Device.objects.filter(user=booking.parent).first()
                if parent_device:
                    url = "https://fcm.googleapis.com/fcm/send"

                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"key={settings.FCM_DJANGO_SETTINGS.get('FCM_SERVER_KEY')}"
                    }
                    body = {
                        "to": f"{parent_device.registration_id}",
                        "notification": {
                            "title": "Pending payment Request",
                            "body": f"{str(booking.nanny.fullname)} has requested for pending payment please pay on time.",
                            "mutable_content": True,
                            "sound": "Tri-tone"
                        },

                        "data": {
                            "url": "<url of media image>",
                            "dl": "<deeplink action on tap of notification>"
                        }
                    }

                    response = requests.post(url, headers=headers, json=body)

                    Notification.objects.create(
                        user=booking.parent,
                        title="Pending Payment Request",
                        body=body,  # Use the body from the Message
                        data={"booking_id": str(booking.id)}
                    )
            else:
                raise ValidationError({
                    'error': 'Payment request cannot be be made when booking is not accepted by you.'
                })
        else:
            raise ValidationError({'error': 'Booking does not exist'})

        return Response('Payment request has been initiated')
