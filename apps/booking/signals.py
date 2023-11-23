from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from fcm_django.models import FCMDevice

from apps.booking.models import Booking
from apps.notification.models import Notification

from firebase_admin.messaging import Message, Notification as FireBaseNotification
import firebase_admin
from firebase_admin import credentials

from apps.users.models import Device
from django.conf import settings
import requests


@receiver(post_save, sender=Booking)
def notify_nanny_on_booking(sender, instance, created, **kwargs):
    if created:
        nanny_device = Device.objects.filter(user=instance.nanny).first()

        if nanny_device:
            url = "https://fcm.googleapis.com/fcm/send"

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"key={settings.FCM_DJANGO_SETTINGS.get('FCM_SERVER_KEY')}"
            }
            body = {
                "to": f"{nanny_device.registration_id}",
                "notification": {
                    "title": "Bravo! New Booking Request",
                    "body": f"New Booking  request from {instance.parent.fullname}",
                    "mutable_content": True,
                    "sound": "Tri-tone"
                },

                "data": {
                    "url": "<url of media image>",
                    "dl": "<deeplink action on tap of notification>"
                }
            }

            response = requests.post(url, headers=headers, json=body)

            Notification.objects.create(
                user=instance.nanny,
                title="New Booking Request",
                body=body,  # Use the body from the Message
                data={"booking_id": str(instance.id)}
            )
