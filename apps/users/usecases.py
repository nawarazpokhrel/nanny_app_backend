import base64

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from django.core.files.base import ContentFile

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
        work_permit_pr = self._data.pop('work_permit_pr')
        first_aid_training_certificate = self._data.pop('first_aid_training_certificate')
        cpr_training_certificate = self._data.pop('cpr_training_certificate')
        elderly_care_training_certificate = self._data.pop('elderly_care_training_certificate')
        nanny_training_certificate = self._data.pop('nanny_training_certificate')
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
        if work_permit_pr:
            format, imgstr = work_permit_pr.split(';base64,')  # Split the base64 data
            ext = format.split('/')[-1]  # Get the file extension
            data = ContentFile(base64.b64decode(imgstr), name=f"{user_profile.id}_work_permit.{ext}")
            user_profile.work_permit_pr.save(data.name, data)
        if first_aid_training_certificate:
            try:
                format, pdf_data = first_aid_training_certificate.split(';base64,')  # Try splitting with ';base64,'
            except ValueError:
                pdf_data = first_aid_training_certificate  # Use the whole string as data if splitting fails

            ext = "pdf"  # PDF file extension
            data = ContentFile(base64.b64decode(pdf_data), name=f"{user_profile.id}_first_aid_training_certificate.{ext}")
            user_profile.first_aid_training_certificate.save(data.name, data)
        if cpr_training_certificate:
            try:
                format, pdf_data = cpr_training_certificate.split(';base64,')  # Try splitting with ';base64,'
            except ValueError:
                pdf_data = cpr_training_certificate  # Use the whole string as data if splitting fails

            ext = "pdf"  # PDF file extension
            data = ContentFile(base64.b64decode(pdf_data),
                               name=f"{user_profile.id}_cpr_training_certificate.{ext}")
            user_profile.cpr_training_certificate.save(data.name, data)
        if nanny_training_certificate:
            try:
                format, pdf_data = nanny_training_certificate.split(';base64,')  # Try splitting with ';base64,'
            except ValueError:
                pdf_data = nanny_training_certificate  # Use the whole string as data if splitting fails

            ext = "pdf"  # PDF file extension
            data = ContentFile(base64.b64decode(pdf_data),
                               name=f"{user_profile.id}_nanny_training_certificate.{ext}")
            user_profile.nanny_training_certificate.save(data.name, data)
        if elderly_care_training_certificate:
            try:
                format, pdf_data = elderly_care_training_certificate.split(';base64,')  # Try splitting with ';base64,'
            except ValueError:
                pdf_data = elderly_care_training_certificate  # Use the whole string as data if splitting fails

            ext = "pdf"  # PDF file extension
            data = ContentFile(base64.b64decode(pdf_data),
                               name=f"{user_profile.id}_elderly_care_training_certificate.{ext}")
            user_profile.elderly_care_training_certificate.save(data.name, data)
        if availabilities:
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

