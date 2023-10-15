from django.contrib.auth import get_user_model
from django.db import models

from apps.common.choices import BookingStatusChoices
from apps.common.models import BaseModel

User = get_user_model()


class Booking(BaseModel):
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parent_bookings',
                               limit_choices_to={'role': 'Parent'})
    nanny = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nanny_bookings',
                              limit_choices_to={'role': 'Nanny'})
    status = models.CharField(BookingStatusChoices,  default=BookingStatusChoices.PENDING)
    date_booked = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    additional_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.parent.fullname} to {self.nanny.fullname}"
