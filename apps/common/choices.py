from django.db import models


class UserRole(models.TextChoices):
    NANNY = 'N', 'Nanny'
    PARENT = 'P', 'Parent'


COUNTRY_CHOICES = (
    ('CA', 'Canada'),
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


class BookingStatusChoices(models.TextChoices):
    PENDING = 'pending', 'Pending'
    ACCEPTED = 'accepted', 'Accepted'
    REJECTED = 'rejected', 'Rejected'
    COMPLETED = 'completed', 'Completed'


class ExpectationTypeChoices(models.TextChoices):
    COOKING = 'cooking', 'Cooking'
    DINING = 'dining', 'Dining'
    HEAVY_LAUNDRY = 'heavy_laundry', 'Heavy Laundry'
    CLEANING = 'cleaning', 'Cleaning Entire House'
    BATHE_CHILDREN = 'bathe_children', 'Bathe and Dress Children'


class ChildCareNeedChoices(models.TextChoices):
    BABY_CARE = 'baby_care', 'Baby Care'
    GRADE_SCHOOL = 'grade_school', 'Grade School'
    TEENAGER = 'teenager', 'Teenager'
    TODDLER = 'toddler', 'Toddler'


