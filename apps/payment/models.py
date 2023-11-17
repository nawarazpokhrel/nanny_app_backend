from django.db import models

from apps.booking.models import Booking
from apps.common.models import BaseModel

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# Create your models here.
User = get_user_model()


class Payment(BaseModel):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=15, choices=[
        ('uncompleted', 'Uncompleted'),
        ('completed', 'Completed')])
    to_be_paid_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Payment for Booking #{self.booking.id} by {str(self.to_be_paid_by)}"

    def clean(self):
        if self.paid_by.role != "P":
            raise ValidationError({"paid_by": "Parent can only pay the booking amount"})

        if self.paid_by != self.booking.parent:
            raise ValidationError({"paid_by": "Parents are not same who booked this nany."})

    def save(self, *args, **kwargs):
        if self.amount is None:
            self.amount = self.booking.calculate_payment()
        super(Payment, self).save(*args, **kwargs)
