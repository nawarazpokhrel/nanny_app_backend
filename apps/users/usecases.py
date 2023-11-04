from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError

from apps.common.usecases import BaseUseCase
from apps.skills.models import TimeSlot
from apps.users.models import UserAvailability, UserProfile

User = get_user_model()


class CreateUserUseCase(BaseUseCase):
    def __init__(self, serializer):
        super().__init__(serializer)

    def _factory(self):
        password = self._data.pop('password')
        user = User(**self._data)
        user.save()
        user.set_password(password)
        user.save()


class CreateUserProfileUseCase(BaseUseCase):
    def __init__(self, serializer, user):
        self._user = user
        super().__init__(serializer)

    def _factory(self):
        commitment_type = self._data.pop('commitment_type')
        skills = self._data.pop('skills')
        availabilities = self._data.pop('availability')
        experience = self._data.pop('experience')
        try:

            user_profile = UserProfile(**self._data, user=self._user)

            user_profile.save()
        except IntegrityError:
            raise ValidationError(
                {
                    'error': 'User already exist.'
                }
            )

        user_profile.commitment_type.add(*commitment_type)
        user_profile.skills.add(*skills)
        user_profile.experience.add(*experience)
        user_profile.save()
        for availability in availabilities:
            date = availability.get('day')
            time_slots = availability.get('timeslots')
            user_availability, created = UserAvailability.objects.get_or_create(
                user_profile=user_profile,
                day=date
            )

            for time_slot_data in time_slots:
                time_slot_name = time_slot_data.get('slug')
                time_slot, created = TimeSlot.objects.get_or_create(slug=time_slot_name)
                user_availability.timeslots.add(time_slot)
            user_availability.save()

