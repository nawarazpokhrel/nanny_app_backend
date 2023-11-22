from django.db import models

from apps.common.models import BaseModel
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Notification(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.CharField(max_length=200)
    data = models.JSONField()

    def __str__(self):
        return self.title
