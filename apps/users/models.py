from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.common.utils import validate_file_size
from apps.users.choices import UserRole, COUNTRY_CHOICES
from apps.users.managers import CustomUserManager
from apps.skills import models


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
        return str(self.fullname)


class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    availability = models.ManyToManyField(models.Availability)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    date_of_birth = models.DateField(null=True)
    country = models.CharField(max_length=5, choices=COUNTRY_CHOICES, default='CA')

    skills = models.ManyToManyField(models.Skills)
    time = models.ManyToManyField(models.Time)
    days = models.ManyToManyField(models.Days)

    has_work_permit = models.BooleanField(default=True)
    workpermit_pr = models.FileField(upload_to='workpermitfile/')

    first_aid_traninig = models.BooleanField(default=False)
    first_aid_traninig_certificate = models.FileField(upload_to='first_aid_traninig_certificate')

    cpr_traning = models.BooleanField(default=False)
    cpr_traning_traninig_certificate = models.FileField(upload_to='cpr_traninig_certificate')

    nanny_traninig = models.BooleanField(default=False)
    nanny_traninig_traninig_certificate = models.FileField(upload_to='nanny_traninig_certificate')

    elderly_care_traninig = models.BooleanField(default=False)
    elderly_care_traninig_certificate = models.FileField(upload_to='elderly_care_traninig_certificate')

    bio = models.TextField()



