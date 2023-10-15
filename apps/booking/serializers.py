from rest_framework import serializers

from apps.booking.models import Booking
from apps.users.serializers import BookingAvailabilitySerializer


class CreateBookingSerializer(serializers.ModelSerializer):
    availability = BookingAvailabilitySerializer(many=True)

    class Meta:
        model = Booking
        fields = [
            'parent',
            'care_needs',
            'commitment',
            'expectations',
            'additional_message',
            'availability'
        ]
