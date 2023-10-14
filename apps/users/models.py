from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.common.utils import validate_file_size
from apps.users.choices import UserRole, COUNTRY_CHOICES
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
        return str(self.fullname)


class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    # availability = models.ManyToManyField('')
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    date_of_birth = models.DateField(null=True)
    country = models.CharField(max_length=5, choices=COUNTRY_CHOICES, default='CA')
