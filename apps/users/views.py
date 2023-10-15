from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.skills.models import TimeSlot
from apps.users import serializers, usecases

from django.contrib.auth import get_user_model

from apps.users.models import UserAvailability, UserProfile
from apps.users.serializers import CreateProfileSerializer, UserPersonalDetailSerializer

User = get_user_model()


# Create your views here.
class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.CreateUserSerializer

    def perform_create(self, serializer):
        return usecases.CreateUserUseCase(serializer=serializer).execute()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = {
            'data': serializer.data,
            'message': 'User created successfully',
            'status_code': status.HTTP_201_CREATED
        }
        return Response(data)


class ListUserView(generics.ListAPIView):
    serializer_class = serializers.ListUserSerializer

    def get_queryset(self):
        return User.objects.all()


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = serializers.ListUserSerializer

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            raise ValidationError(
                {'error': 'user does not exist for following id.'}
            )


class CreateUserProfileView(generics.CreateAPIView):
    serializer_class = CreateProfileSerializer

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            raise ValidationError(
                {'error': 'user does not exist for following id.'}
            )

    def perform_create(self, serializer):
        commitment_type = serializer.validated_data.pop('commitment_type')
        skills = serializer.validated_data.pop('skills')
        availabilities = serializer.validated_data.pop('availability')
        try:

            user_profile = UserProfile(**serializer.validated_data, user=self.get_object())

            user_profile.save()
        except IntegrityError:
            raise ValidationError(
                {
                    'error': 'User already exist.'
                }
            )

        user_profile.commitment_type.add(*commitment_type)
        user_profile.skills.add(*skills)
        user_profile.save()
        for availability in availabilities:
            day = availability.get('day')
            time_slots = availability.get('timeslots')

            # Create or Get the UserAvailability object for the given day
            user_availability, created = UserAvailability.objects.get_or_create(
                user_profile=user_profile,
                day=day
            )

            for time_slot_data in time_slots:
                time_slot_name = time_slot_data.get('name')
                time_slot, created = TimeSlot.objects.get_or_create(name=time_slot_name)
                user_availability.timeslots.add(time_slot)
            user_availability.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = {
            "message": "User profile created successfully",
            "status": status.HTTP_201_CREATED
        }
        return Response(data)


class ListUserPersonalDetailView(generics.ListAPIView):
    serializer_class = UserPersonalDetailSerializer

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            raise ValidationError(
                {'error': 'user does not exist for following id.'}
            )

    def get_queryset(self):
        return User.objects.filter(pk=self.get_object().id)


class UserPersonalDetailView(generics.RetrieveAPIView):
    serializer_class = UserPersonalDetailSerializer

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            raise ValidationError(
                {'error': 'user does not exist for following id.'}
            )


