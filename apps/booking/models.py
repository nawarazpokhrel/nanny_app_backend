from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Count, Sum

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
        return f"Booking #{self.id} - {self.parent.fullname} to {self.nanny.fullname}"


    def clean(self):
        if self.parent:
            if self.parent.role == 'N':
                raise ValidationError(
                    {
                        'parent': "Parent  cannot  to be Nanny"
                    }
                )
        if self.nanny:
            if self.nanny.role == 'P':
                raise ValidationError(
                    {
                        'nanny': "Nanny   cannot  to be parent"
                    }
                )
        booking = Booking.objects.filter(
            parent=self.parent,
            nanny=self.nanny,
            status='pending'
        ).exists()
        if booking:
            raise ValidationError({
                'status': 'Cannot make next booking until your request is accepted or rejected by this nanny.'
            }
            )


    @property
    def calculate_days_worked(self):
        # Count the number of unique dates the user worked
        days_worked = self.dates.values('date').distinct().count()
        return days_worked

    @property
    def calculate_total_hours_worked(self):
        # Count the number of time slots and assume each slot represents 4 hours
        total_hours_worked = self.dates.aggregate(total_slots=Count('time_slots'))['total_slots']

        # Assuming 1 slot = 4 hours
        total_hours_worked *= 4

        return total_hours_worked

    def calculate_payment(self):
        # Aggregate bookings based on date and time slots using Django ORM
        aggregated_data = self.dates.values('date').annotate(
            time_slots_count=Count('time_slots'),
        )

        total_payment = 0

        for entry in aggregated_data:
            if self.nanny.userprofile:
                time_slots_count = entry['time_slots_count']

                # Assuming the duration is always 4 hours for both morning and evening time slots
                total_hours = time_slots_count * 4

                nanny_hourly_price = self.nanny.userprofile.amount_per_hour if self.nanny.role == 'N' else 0

                entry_total_payment = total_hours * nanny_hourly_price
                total_payment += entry_total_payment  # Accumulate the total payment for each entry
            else:
                raise ValidationError({'non_field_error': "Nanny has not set amount per hour."})

        return total_payment

    @property
    def total_amount(self):
        """
        calculate total amount nanny will be getting
        """
        return float(self.calculate_payment())


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
