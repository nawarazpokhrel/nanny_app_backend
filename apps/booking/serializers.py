from rest_framework import serializers

from apps.booking.models import Booking, BookingDate, Review
from apps.skills.serializers import ChildCareNeedSerializer, ListSkillSerializer, ListAvailabilitySerializer
from apps.users.serializers import BookingAvailabilitySerializer, ListUserSerializer, TimeSlotSerializer, \
    UserPersonalDetailSerializer


class CreateBookingSerializer(serializers.ModelSerializer):
    availability = BookingAvailabilitySerializer(many=True)

    class Meta:
        model = Booking
        fields = [
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
    parent = serializers.SerializerMethodField()
    nanny = serializers.SerializerMethodField()
    commitment = ListAvailabilitySerializer()
    expectations = ListSkillSerializer(many=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    booking_dates = BookingAvailabilitySerializer(source='dates', many=True)
    total_amount = serializers.FloatField()
    has_reviewed = serializers.BooleanField()
    has_payment_done = serializers.BooleanField()

    class Meta:
        model = Booking
        fields = [
            'id',
            'parent',
            'nanny',
            'care_needs',
            'expectations',
            'additional_message',
            'commitment',
            'status',
            'booking_dates',
            'total_amount',
            'has_reviewed',
            'has_payment_done',
        ]

    def get_parent(self, obj):
        return ListUserSerializer(instance=obj.parent, context=self.context.get('request').__dict__).data

    def get_nanny(self, obj):
        return UserPersonalDetailSerializer(instance=obj.nanny, context=self.context).data

    def get_has_paid(self, obj):
        print(self.context)


class AcceptBookingSerializer(serializers.ModelSerializer):
    STATUS_CHOICES = [
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    status = serializers.ChoiceField(choices=STATUS_CHOICES)

    class Meta:
        model = Booking
        fields = ('status',)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['rating', 'message']
        model = Review
