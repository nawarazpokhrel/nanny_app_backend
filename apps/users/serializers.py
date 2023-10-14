from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.skills.models import TimeSlot
from apps.users.models import UserProfile, UserAvailability

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'phone_number',
            'fullname',
            'role',
            'password'

        ]


class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'groups', 'user_permissions')


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ('id', 'name')


class UserAvailabilitySerializer(serializers.ModelSerializer):
    timeslots = TimeSlotSerializer(many=True)

    class Meta:
        model = UserAvailability
        fields = ('day', 'timeslots')


class CreateProfileSerializer(serializers.ModelSerializer):
    availability = UserAvailabilitySerializer(source='useravailability_set', many=True)
    class Meta:
        model = UserProfile
        fields = [
            'commitment_type',
            'gender',
            'date_of_birth',
            'country',
            'address_line_1',
            'postal_code',
            'skills',
            'has_work_permit',
            'work_permit_pr',
            'has_first_aid_training',
            'first_aid_training_certificate',
            'has_cpr_training',
            'cpr_training_certificate',
            'has_nanny_training',
            'nanny_training_certificate',
            'has_elderly_care_training',
            'elderly_care_training_certificate',
            'bio',
            'availability'

        ]
