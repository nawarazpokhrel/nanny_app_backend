from django.urls import path
from apps.payment.views import ListPaymentDetailView,CreatePaymentView
urlpatterns = [
    path(
        'booking/<int:booking_id>/detail',
        ListPaymentDetailView.as_view()
    ),
    path('booking/<int:booking_id>/create',
         CreatePaymentView.as_view()
         )

]
