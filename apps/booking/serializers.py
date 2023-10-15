from rest_framework import serializers

from apps.booking.models import Booking


class AddBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
