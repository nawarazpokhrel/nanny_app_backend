from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from apps.common.choices import RatingChoices
from apps.common.models import BaseModel
from apps.skills.models import Experience, Availability, Expectation, TimeSlot, Skills

User = get_user_model()


class Booking(BaseModel):
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parent_bookings')
    nanny = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nanny_bookings')
    care_needs = models.ManyToManyField(Experience)
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
        print(self.calculate_payment())
        return f"Booking #{self.id} - {self.parent.fullname} to {self.nanny.fullname}"

    def clean(self):
        if self.parent.role == 'N':
            raise ValidationError(
                {
                    'parent': "Parent  cannot  to be Nanny"
                }
            )
        if self.nanny.role == 'P':
            raise ValidationError(
                {
                    'nanny': "Nanny   cannot  to be parent"
                }
            )

    def calculate_payment(self):
        # Calculate payment based on user per hour price, days, and time slots
        total_hours = 0

        for booking_date in self.dates.all():
            days_difference = (booking_date.date - timezone.now().date()).days + 1
            for time_slot in booking_date.time_slots.all():
                # Adjust this line based on your TimeSlot model's actual structure
                total_hours += time_slot.duration_in_hours if hasattr(time_slot, 'duration_in_hours') else 0

        parent_hourly_price = self.parent.userprofile.amount_per_hour if self.parent.role == 'N' else 0
        nanny_hourly_price = self.nanny.userprofile.amount_per_hour if self.nanny.role == 'P' else 0

        total_payment = total_hours * (parent_hourly_price + nanny_hourly_price)

        return total_payment

        return total_payment


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
