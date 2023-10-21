from django.contrib import admin

from apps.booking.models import Booking, BookingDate, Review

# Register your models here.
admin.site.register(Booking)
admin.site.register(BookingDate)
admin.site.register(Review)
