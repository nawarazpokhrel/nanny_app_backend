from apps.booking.models import Booking
from django_filters import rest_framework as filters


class BookingFilter(filters.FilterSet):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed')
    ]
    # full_name = filters.CharFilter(method='filter_full_name')
    status = filters.ChoiceFilter(choices=STATUS_CHOICES)

    class Meta:
        model = Booking
        fields = [
            'status'
        ]

    def filter_full_name(self, queryset, name, value):
        # Check user role
        if self.request.user.role == 'P':
            # If user is parent, filter by nanny full name
            return queryset.filter(nanny__user_detail__full_name__icontains=value)
        elif self.request.user.role == 'N':
            # If user is nanny, filter by parent full name
            return queryset.filter(parent__user_detail__full_name__icontains=value)
        else:
            # If user role is neither 'P' nor 'N', return the original queryset
            return queryset
