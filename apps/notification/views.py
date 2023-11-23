from django.shortcuts import render

# Create your views here.

from rest_framework import generics

from apps.notification.models import Notification
from apps.notification.serializers import NotificationSerializer

from rest_framework.permissions import IsAuthenticated


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
