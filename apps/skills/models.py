from django.db import models

from apps.common.choices import ExpectationTypeChoices, ChildCareNeedChoices
from apps.common.models import BaseModel
from apps.common import choices
from django.utils.text import slugify


# Create your models here.


class Availability(BaseModel):
    availability = models.CharField(max_length=50, choices=choices.COMMIT_CHOICES, unique=True)

    def __str__(self):
        return self.get_availability_display()

    @property
    def name(self):
        return self.get_availability_display()


class Skills(BaseModel):
    skills = models.CharField(max_length=100, choices=choices.SKILL_CHOICES, )

    def __str__(self):
        return self.get_skills_display()

    @property
    def name(self):
        return self.get_skills_display()


class TimeSlot(BaseModel):
    name = models.CharField(max_length=50, choices=choices.TIME_CHOICES)
    slug = models.SlugField(unique=True, blank=True,null=True,editable=False)  # Add a SlugField

    def __str__(self):
        return self.get_name_display()

    @property
    def timeslot_value(self):
        return self.get_name_display()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.get_name_display())
        super(TimeSlot, self).save(*args, **kwargs)


class Days(BaseModel):
    day_name = models.CharField(max_length=20, choices=choices.DAY_CHOICES, unique=True)

    def __str__(self):
        return self.get_day_name_display()

    @property
    def day_value(self):
        return self.get_day_name_display()


class Expectation(BaseModel):
    TYPES = [
        ('cooking', 'Cooking'),
        ('dining', 'Dining'),
        ('heavy_laundry', 'Heavy Laundry'),
        ('cleaning', 'Cleaning Entire House'),
        ('bathe_children', 'Bathe and Dress Children')
    ]
    type = models.CharField(
        choices=ExpectationTypeChoices.choices,
        max_length=50
    )

    def __str__(self):
        return self.get_type_display()

    @property
    def type_value(self):
        return self.get_type_display()


class Experience(BaseModel):
    type = models.CharField(
        choices=ChildCareNeedChoices.choices,
        max_length=20
    )

    def __str__(self):
        return self.get_type_display()

    @property
    def type_value(self):
        return self.get_type_display()
