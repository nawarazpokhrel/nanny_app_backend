from django.contrib.auth import get_user_model
from django.db import models

from apps.common.choices import BookingStatusChoices, RatingChoices
from apps.common.models import BaseModel
from django.core.exceptions import ValidationError
from apps.skills.models import ChildCareNeed, Availability, Expectation, TimeSlot, Skills

User = get_user_model()


class Booking(BaseModel):
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parent_bookings')
    nanny = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nanny_bookings')
    care_needs = models.ManyToManyField(ChildCareNeed)
    commitment = models.ForeignKey(Availability, on_delete=models.CASCADE, null=True)
    expectations = models.ManyToManyField(Skills)
    additional_message = models.TextField(blank=True, null=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed')
    ]
    status = models.CharField(choices=STATUS_CHOICES, default='pending', max_length=10)

    def __str__(self):
        return f"Booking #{self.id} - {self.parent.fullname} to {self.nanny.fullname}"


class BookingDate(BaseModel):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='dates')
    date = models.DateField()
    time_slots = models.ManyToManyField(TimeSlot)

    def __str__(self):
        time_slots = ", ".join([slot.name for slot in self.time_slots.all()])
        return f"Booking ID: {self.booking.id} | Date: {self.date} | Time slots: {time_slots}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['booking', 'date'], name='unique_booking_date')
        ]


class Review(BaseModel):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.CharField(max_length=5, choices=RatingChoices.choices)
    message = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.user.fullname} ->{self.rating}'

    def clean(self):
        if self.user.role != 'P':
            raise ValidationError(
                {
                    'user': "User need to be Parent to review"
                }
            )
