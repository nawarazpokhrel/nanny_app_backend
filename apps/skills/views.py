from django.shortcuts import render

from rest_framework.generics import ListAPIView
from apps.skills.models import Availability, Skills, TimeSlot, Days, Expectation
from apps.skills.serializers import ListAvailabilitySerializer, ListSkillSerializer, ListTimeSlotSerializer, \
    ListDaysSerializer, ListExpectationSerializer, CitySerializer
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


class CityListView(APIView):
    def get(self, request):
        cities = [
            {"city": "Toronto", "short_name": "Tor"},
            {"city": "Vancouver", "short_name": "Van"},
            {"city": "Montreal", "short_name": "Mon"},
            {"city": "Calgary", "short_name": "Cal"},
            {"city": "Edmonton", "short_name": "Edm"},
            {"city": "Ottawa", "short_name": "Ott"},
            {"city": "Quebec City", "short_name": "Que"},
            {"city": "Winnipeg", "short_name": "Win"},
            {"city": "Halifax", "short_name": "Hal"},
            {"city": "Victoria", "short_name": "Vic"},
        ]

        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)