from apps.booking.models import Booking
from django_filters import rest_framework as filters


class BookingFilter(filters.FilterSet):
    class Meta:
        model = Booking
        fields = {
            'status': ['exact', 'in'],
        }
