from rest_framework import serializers

from apps.booking.models import Booking, BookingDate
from apps.common.utils import ChoiceField
from apps.skills.serializers import ChildCareNeedSerializer, ListSkillSerializer, ListAvailabilitySerializer
from apps.users.serializers import BookingAvailabilitySerializer, ListUserSerializer, TimeSlotSerializer


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


class BookingDateSerializer(serializers.ModelSerializer):
    timeslots = TimeSlotSerializer(many=True)

    class Meta:
        model = BookingDate
        fields = ('day', 'timeslots', 'booking')


class ListBookingSerializer(serializers.ModelSerializer):
    care_needs = ChildCareNeedSerializer(many=True)
    parent = ListUserSerializer()
    commitment = ListAvailabilitySerializer()
    expectations = ListSkillSerializer(many=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    booking_dates = BookingAvailabilitySerializer(source='dates', many=True)

    class Meta:
        model = Booking
        fields = [
            'id',
            'parent',
            'care_needs',
            'expectations',
            'additional_message',
            'commitment',
            'status',
            'booking_dates'
        ]


class AcceptBookingSerializer(serializers.ModelSerializer):
    STATUS_CHOICES = [
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    status = serializers.ChoiceField(choices=STATUS_CHOICES)

    class Meta:
        model = Booking
        fields = ('status',)
