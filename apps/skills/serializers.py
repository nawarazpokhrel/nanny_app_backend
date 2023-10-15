from rest_framework import serializers

from apps.common.utils import ChoiceField
from apps.skills.models import Availability, Skills, TimeSlot, Days

from apps.common import choices


class ListAvailabilitySerializer(serializers.ModelSerializer):
    name = ChoiceField(choices=choices.COMMIT_CHOICES, source='availability')

    class Meta:
        model = Availability
        fields = ('name', 'id')


class ListSkillSerializer(serializers.ModelSerializer):
    name = ChoiceField(choices=choices.SKILL_CHOICES,source='skills')

    class Meta:
        model = Skills
        fields = ('name', 'id')


class ListTimeSlotSerializer(serializers.ModelSerializer):
    name = ChoiceField(choices=choices.TIME_CHOICES)

    class Meta:
        model = TimeSlot
        fields = ('name', 'id')


class ListDaysSerializer(serializers.ModelSerializer):
    name = ChoiceField(choices=choices.DAY_CHOICES,source='day_name')

    class Meta:
        model = Days
        fields = ('name', 'id')
