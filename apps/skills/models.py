from django.db import models
from apps.common.models import BaseModel
from apps.common import choices


# Create your models here.


class Availability(BaseModel):
    availability = models.CharField(max_length=50, choices = choices.COMMIT_CHOICES)
    


class Skills(BaseModel):
    
    Skills = models.CharField(max_length=100, choices=choices.SKILL_CHOICES,)


class Time(BaseModel):

    time_slot = models.CharField(max_length=50, choices=choices.TIME_CHOICES, unique=True)


class Days(BaseModel):

    day_name = models.CharField(max_length=20, choices=choices.DAY_CHOICES, unique=True)
    time_slot = models.ForeignKey(Time, on_delete=models.CASCADE)



  