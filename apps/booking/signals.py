from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from fcm_django.models import FCMDevice

from apps.booking.models import Booking
from apps.notification.models import Notification

from firebase_admin.messaging import Message, Notification as FireBaseNotification
import firebase_admin
from firebase_admin import credentials

@receiver(post_save, sender=Booking)
def notify_nanny_on_booking(sender, instance, created, **kwargs):
    if created:
        nanny_device = FCMDevice.objects.filter(user=instance.nanny).first()

        if not firebase_admin._apps:
            # Re-initialize Firebase Admin SDK if not initialized
            cred = credentials.Certificate("serviceAccountKey.json")
            firebase_admin.initialize_app(cred)

        if nanny_device:
            message = Message(
                notification=FireBaseNotification(
                    title="New Booking Request",
                    body=f"You have a new booking request from {instance.parent.fullname}",
                ),
                data={
                    "booking_id": str(instance.id),
                    "custom_key": "custom_value",
                },
            )

            nanny_device.send_message(message)

            Notification.objects.create(
                user=instance.nanny,
                title="New Booking Request",
                body=message.notification.body,  # Use the body from the Message
                data={"booking_id": str(instance.id)}
            )
