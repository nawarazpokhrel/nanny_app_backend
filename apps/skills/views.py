from django.shortcuts import render

from rest_framework.generics import ListAPIView
from apps.skills.models import Availability, Skills, TimeSlot, Days, Expectation, Experience
from apps.skills.serializers import ListAvailabilitySerializer, ListSkillSerializer, ListTimeSlotSerializer, \
    ListDaysSerializer, ListExpectationSerializer, CitySerializer, ChildCareNeedSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.views import  APIView
from rest_framework.response import  Response
from rest_framework import status
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


class ListExperienceView(ListAPIView):
    serializer_class = ChildCareNeedSerializer

    def get_queryset(self):
        return Experience.objects.all()


class CityListView(APIView):
    def get(self, request):
        cities = [
            {"city": "Toronto", "short_name": "TOR"},
            {"city": "Vancouver", "short_name": "VAN"},
            {"city": "Montreal", "short_name": "MON"},
            {"city": "Calgary", "short_name": "CAL"},
            {"city": "Edmonton", "short_name": "EDM"},
            {"city": "Ottawa", "short_name": "OTT"},
            {"city": "Quebec City", "short_name": "QUE"},
            {"city": "Winnipeg", "short_name": "WIN"},
            {"city": "Halifax", "short_name": "HAL"},
            {"city": "Victoria", "short_name": "VIC"},
        ]

        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)