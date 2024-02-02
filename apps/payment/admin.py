from django.contrib import admin

from apps.payment.models import Payment, PaymentMethod

# Register your models here.
admin.site.register(Payment)
admin.site.register(PaymentMethod)
