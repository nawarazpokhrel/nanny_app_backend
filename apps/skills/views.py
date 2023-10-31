from django.shortcuts import render

from rest_framework.generics import ListAPIView
from apps.skills.models import Availability, Skills, TimeSlot, Days, Expectation
from apps.skills.serializers import ListAvailabilitySerializer, ListSkillSerializer, ListTimeSlotSerializer, \
    ListDaysSerializer, ListExpectationSerializer
from rest_framework.exceptions import ValidationError


# Create your views here.


class ListAvailiabilityView(ListAPIView):
    serializer_class = ListAvailabilitySerializer

    def get_queryset(self):
        return Availability.objects.all()


class ListSkillView(ListAPIView):
    serializer_class = ListSkillSerializer

    def get_queryset(self):
        return Skills.objects.all()


class LisTimeSlotView(ListAPIView):
    serializer_class = ListTimeSlotSerializer

    def get_queryset(self):
        return TimeSlot.objects.all()


class ListDaysView(ListAPIView):
    serializer_class = ListDaysSerializer

    def get_queryset(self):
        return Days.objects.all()


class ListExpectationView(ListAPIView):
    serializer_class = ListExpectationSerializer

    def get_queryset(self):
        return Expectation.objects.all()
