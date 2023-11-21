from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from fcm_django.models import FCMDevice

from apps.booking.models import Booking


@receiver(post_save, sender=Booking)
def notify_nanny_on_booking(sender, instance, created, **kwargs):
    if created:
        nanny_device = FCMDevice.objects.filter(user=instance.nanny).first()
        if nanny_device:
            title = "New Booking Request"
            body = f"You have a new booking request from {instance.parent.fullname}."
            data = {"booking_id": instance.id}
            nanny_device.send_message(title=title, body=body, data=data)
        else:
            raise ValidationError({'error': 'Nanny device not found for notification.'})