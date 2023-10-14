from rest_framework import serializers
from apps.skills.models import Availability, Skills, TimeSlot, Days

class ListAvailiabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ('availability', 'id')


class ListSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = ('skills', 'id')


class ListTimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ('name', 'id')


class ListDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Days
        fields = ('day_name', 'id')