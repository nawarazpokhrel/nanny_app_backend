from django.db import models


class UserRole(models.TextChoices):
    NANNY = 'N', 'Nanny'
    PARENT = 'P', 'Parent'


COUNTRY_CHOICES = (
    ('CA','Canada'),
)


COMMIT_CHOICES = (
    ('F', 'Full Time'),
    ('P', 'Part Time'),
)


SKILL_CHOICES = (
    ('C', 'Cooking'),
    ('D', 'Driving'),
    ('HL', 'Heavy Laundry'),
    ('CH', 'Cleaning entire house'),
    ('BD', 'Bath and dress children'),
)

TIME_CHOICES = (
    ('MOR', 'Morning'),
    ('AFT', 'Afternoon'),
    ('EVE', 'Evening'),
    ('NIG', 'Night'),
)


DAY_CHOICES = (
    ('SUN', 'Sunday'),
    ('MON', 'Monday'),
    ('TUE', 'Tuesday'),
    ('WED', 'Wednesday'),
    ('THU', 'Thursday'),
    ('FRI', 'Friday'),
    ('SAT', 'Saturday'),
)


