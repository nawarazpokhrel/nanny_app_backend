from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import Avg
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.common.choices import UserRole, COUNTRY_CHOICES, CanadaCity, RatingChoices
from apps.common.models import BaseModel
from apps.common.utils import validate_file_size

from apps.skills.models import Availability, Skills, Days, TimeSlot, Expectation
from apps.users.managers import CustomUserManager


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)
    fullname = models.CharField(_('full name'), max_length=255, blank=True, null=True)
    avatar = models.ImageField(null=True, blank=True, default='arthik_default_user.jpeg',
                               validators=[validate_file_size])
    role = models.CharField(max_length=10, choices=UserRole.choices, default=UserRole.NANNY)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['fullname']

    objects = CustomUserManager()

    def __str__(self):
        return f'{str(self.fullname)}-> {self.role}'

    @property
    def has_user_profile(self):
        if hasattr(self, 'userprofile'):
            return True
        else:
            return False

    # @property
    # def review_rating(self):
    #     self.nanny_bookings_set.filter()
    @property
    def average_rating(self):
        from apps.booking.models import Review

        if self.role == 'N':
            # Calculate the average rating for the user's reviews
            rating_mapping = {
                RatingChoices.ONE: 1,
                RatingChoices.TWO: 2,
                RatingChoices.THREE: 3,
                RatingChoices.FOUR: 4,
                RatingChoices.FIVE: 5,
            }

            # Calculate the average rating for the user's reviews
            reviews = Review.objects.filter(booking__nanny=self)

            # Calculate the average using the mapped values
            total = sum(rating_mapping[review.rating] for review in reviews)
            average = total / len(reviews) if len(reviews) > 0 else 0
            return average
        else:
            return None




class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    commitment_type = models.ManyToManyField(Availability)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    amount_per_hour = models.PositiveIntegerField(null=True)
    country = models.CharField(max_length=5, choices=COUNTRY_CHOICES, default='CA')
    address = models.CharField(
        max_length=100,
        choices=CanadaCity.choices,
        null=True,
        blank=True
    )
    expectation = models.ManyToManyField(Expectation)
    postal_code = models.CharField(max_length=100, null=True, blank=True)

    skills = models.ManyToManyField(Skills)

    has_work_permit = models.BooleanField(default=True)
    work_permit_pr = models.FileField(null=True, blank=True)

    has_first_aid_training = models.BooleanField(default=False)
    first_aid_training_certificate = models.FileField(null=True, blank=True)

    has_cpr_training = models.BooleanField(default=False)
    cpr_training_certificate = models.FileField(null=True, blank=True)

    has_nanny_training = models.BooleanField(default=False)
    nanny_training_certificate = models.FileField(null=True, blank=True)

    has_elderly_care_training = models.BooleanField(default=False)
    elderly_care_training_certificate = models.FileField(null=True, blank=True)

    bio = models.TextField(null=True, blank=True)
    favorites = models.ManyToManyField(User, related_name='favorite_nannies', blank=True)
    def __str__(self):
        return f'{self.user.fullname}->role {self.user.role}'


class UserAvailability(BaseModel):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    day = models.ForeignKey(Days, on_delete=models.CASCADE)
    timeslots = models.ManyToManyField(TimeSlot)

    class Meta:
        unique_together = ('user_profile', 'day')

    def __str__(self):
        time_slots = ", ".join([slot.name for slot in self.timeslots.all()])
        return f"{self.user_profile.user.fullname} -> {self.day.day_name} -> {time_slots}"































