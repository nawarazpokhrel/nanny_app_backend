from rest_framework import serializers

from apps.common.utils import ChoiceField
from apps.skills.models import Availability, Skills, TimeSlot, Days, Expectation, Experience

from apps.common import choices


class ListAvailabilitySerializer(serializers.ModelSerializer):
    # name = ChoiceField(choices=choices.COMMIT_CHOICES, source='availability')

    class Meta:
        model = Availability
        fields = ('name', 'id')


class ListSkillSerializer(serializers.ModelSerializer):
    # name = ChoiceField(choices=choices.SKILL_CHOICES, source='skills')

    class Meta:
        model = Skills
        fields = ('name', 'id')


class ListTimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ('name', 'timeslot_value', 'id', 'slug')


class ListDaysSerializer(serializers.ModelSerializer):
    day_value = serializers.CharField()

    # name = ChoiceField(choices=choices.DAY_CHOICES,source='day_name')

    class Meta:
        model = Days
        fields = ('day_name', 'id', 'day_value')


class ChildCareNeedSerializer(serializers.ModelSerializer):
    # name = ChoiceField(choices=choices.DAY_CHOICES,source='day_name')

    class Meta:
        model = Experience
        fields = ('type', 'id', 'type_value')


class ListExpectationSerializer(serializers.ModelSerializer):
    # type_value = serializers.CharField(
    class Meta:
        model = Expectation
        fields = [
            'id',
            'type',
            'type_value'
        ]


class CitySerializer(serializers.Serializer):
    city = serializers.CharField()
    short_name = serializers.CharField()
