import base64
import binascii
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.utils import timezone
from apps.common.usecases import BaseUseCase
from apps.pyotp.mixins import OTPMixin
from apps.pyotp.models import PyOTP
from apps.skills.models import TimeSlot
from apps.users.emails import SendActivationEmail
from apps.users.models import UserAvailability, UserProfile

User = get_user_model()


class CreateUserUseCase(BaseUseCase, OTPMixin):
    def __init__(self, serializer):
        super().__init__(serializer)

    def _factory(self):
        password = self._data.pop('password')
        email = self._data.get('email')
        email_exists = User.objects.filter(email=email).first()
        if email_exists:
            raise ValidationError({'error': "User with this email already exists"})

        user = User(**self._data)
        user.is_active = False
        user.save()
        user.set_password(password)
        user.save()
        self.send_email(user)

    def send_email(self, user):
        code = self._generate_totp(
            user=user,
            purpose='A',
            interval=120
        )
        SendActivationEmail(
            context={
                'name': user.fullname,
                'token': code

            }
        ).send(to=[user.email])


class CreateUserProfileUseCase(BaseUseCase):
    def __init__(self, serializer, user):
        self._user = user
        self.first_aid_training_certificate = None
        self.cpr_training_certificate = None
        self.elderly_care_training_certificate = None
        self.nanny_training_certificate = None
        super().__init__(serializer)

    def _factory(self):

        commitment_type = self._data.pop('commitment_type')
        work_permit_pr = self._data.pop('work_permit_pr')
        if self._data.get('first_aid_training_certificate'):
            self.first_aid_training_certificate = self._data.pop('first_aid_training_certificate')
        if self._data.get('cpr_training_certificate'):
            self.cpr_training_certificate = self._data.pop('cpr_training_certificate')
        if self._data.get('elderly_care_training_certificate'):
            self.elderly_care_training_certificate = self._data.pop('elderly_care_training_certificate')
        if self._data.get('nanny_training_certificate'):
            self.nanny_training_certificate = self._data.pop('nanny_training_certificate')
        skills = self._data.pop('skills')
        availabilities = self._data.pop('availability')
        experience = self._data.pop('experience')
        try:
            user_profile = UserProfile(**self._data, user=self._user)
            try:
                # Decode base64 string to binary data
                binary_data = base64.b64decode(work_permit_pr)
                file_content = ContentFile(binary_data)
                user_profile.work_permit_pr.save(f'{user_profile.user.fullname}_work-permit.pdf', file_content)

                if self.cpr_training_certificate:
                    binary_data = base64.b64decode(self.cpr_training_certificate)
                    file_content = ContentFile(binary_data)
                    user_profile.cpr_training_certificate.save(
                        f'{user_profile.user.fullname}cpr_training_certificate.pdf', file_content,
                    )
                if self.elderly_care_training_certificate:
                    binary_data = base64.b64decode(self.elderly_care_training_certificate)
                    file_content = ContentFile(binary_data)
                    user_profile.elderly_care_training_certificate.save(
                        f'{user_profile.user.fullname}elderly_care_training_certificate.pdf', file_content,
                    )
                if self.nanny_training_certificate:
                    binary_data = base64.b64decode(self.nanny_training_certificate)
                    file_content = ContentFile(binary_data)
                    user_profile.nanny_training_certificate.save(
                        f'{user_profile.user.fullname}nanny_training_certificate.pdf', file_content,
                        save=True)
            except (TypeError, binascii.Error) as e:
                raise ValidationError({'error': 'Unable to load base64 to file'})
            except Exception as e:
                # Handle other unexpected exceptions
                print(f"Unexpected error: {e}")
                raise ValidationError({'error': 'An error occurred during file saving Unexpected error: {e}'})
            user_profile.commitment_type.add(*commitment_type)
            user_profile.skills.add(*skills)
            user_profile.experience.add(*experience)
            user_profile.save()
        except IntegrityError:
            raise ValidationError(
                {
                    'error': 'User already exist.'
                }
            )

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


class ResendOTPUsecase(BaseUseCase, OTPMixin):
    """
    Use this endpoint to resend otp
    """

    def __init__(self, serializer):
        self._serializer = serializer
        super().__init__(self._serializer)
        self.user = User.objects.filter(email=self._data.get('email')).first()

    def execute(self):
        self._is_valid()
        self._factory()

    def _is_valid(self):
        # wait for 2 minutes.
        if self.user is None:
            raise ValidationError({
                'error': 'user doesnot exist for following id'
            })
        try:
            old_otp = PyOTP.objects.get(
                user=self.user,
                purpose='A'
            )
        except PyOTP.DoesNotExist:
            raise ValidationError({
                'non_field_errors': 'Following email Has no old OTP'
            })

        if old_otp.created_at + timedelta(minutes=2) > timezone.now():
            raise ValidationError({
                'non_field_errors': 'OTP Resend  can be performed only after 2 minutes.'
            })

    def _factory(self):
        if self.user:
            code = self._regenerate_totp(self.user, 'A')
            SendActivationEmail(
                context={
                    'name': self.user.fullname,
                    'token': code

                }
            ).send(to=[self.user.email])
