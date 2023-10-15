from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.common import choices
from apps.common.choices import UserRole
from apps.common.utils import ChoiceField
from apps.skills.models import TimeSlot
from apps.skills.serializers import ListSkillSerializer, ListAvailabilitySerializer, ListDaysSerializer
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
    role = ChoiceField(choices=UserRole.choices)

    class Meta:
        model = User
        exclude = ('password', 'groups', 'user_permissions')


class TimeSlotSerializer(serializers.ModelSerializer):
    name = ChoiceField(choices=choices.TIME_CHOICES)

    class Meta:
        model = TimeSlot
        fields = ('id', 'name')


class UserAvailabilitySerializer(serializers.ModelSerializer):
    timeslots = TimeSlotSerializer(many=True)
    day = ListDaysSerializer()

    class Meta:
        model = UserAvailability
        fields = ('day', 'timeslots')


class CreateProfileSerializer(serializers.ModelSerializer):
    availability = UserAvailabilitySerializer(many=True)

    class Meta:
        model = UserProfile
        fields = [
            'commitment_type',
            'gender',
            'date_of_birth',
            'country',
            'address_line_1',
            'amount_per_hour',
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

    def validate_availability(self, value):
        days = [availability['day'] for availability in value]
        if len(days) != len(set(days)):
            raise serializers.ValidationError("Duplicate days are not allowed in availability.")
        return value


# {
#     "commitment_type": [
#         1,
#         2
#     ],
#     "gender": "M",
#     "date_of_birth": "2023-10-25",
#     "country": "CA",
#     "address_line_1": "12",
#     "postal_code": "12",
#     "skills": [
#         1,
#         2
#     ],
#     "has_work_permit": false,
#     "work_permit_pr": null,
#     "amount_per_hour": 25,
#     "has_first_aid_training": false,
#     "first_aid_training_certificate": null,
#     "has_cpr_training": false,
#     "cpr_training_certificate": null,
#     "has_nanny_training": false,
#     "nanny_training_certificate": null,
#     "has_elderly_care_training": false,
#     "elderly_care_training_certificate": null,
#     "bio": "ok",
# "availability": [
#     {
#       "day": 1,
#       "timeslots": [
#         {
#           "name": "MOR"
#         }
#       ]
#     }
#   ]
# }

class UserPersonalProfileSerializer(serializers.ModelSerializer):
    commitment_type = ListAvailabilitySerializer(many=True)
    skills = ListSkillSerializer(many=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = ChoiceField(choices=GENDER_CHOICES)
    country = ChoiceField(choices=choices.COUNTRY_CHOICES)
    availability = UserAvailabilitySerializer(source='useravailability_set', many=True)
    user_id = serializers.IntegerField(source='user.id')

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'user_id',
            'commitment_type',
            'gender',
            'date_of_birth',
            'amount_per_hour',
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


class UserPersonalDetailSerializer(serializers.ModelSerializer):
    user_detail = serializers.SerializerMethodField()

    personal_detail = UserPersonalProfileSerializer(source='userprofile')

    class Meta:
        model = User
        fields = [
            'user_detail',
            'personal_detail'
        ]

    def get_user_detail(self, obj):
        return ListUserSerializer(instance=obj).data
