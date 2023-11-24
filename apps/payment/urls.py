from django.urls import path
from apps.payment.views import ListPaymentDetailView, CreatePaymentView, PaymentMethodView, RequestForPaymentView

urlpatterns = [
    path(
        'booking/<int:booking_id>/detail',
        ListPaymentDetailView.as_view()
    ),
    path(
        'booking/<int:booking_id>/request-payment',
        RequestForPaymentView.as_view()
    ),
    path('booking/<int:booking_id>/create',
         CreatePaymentView.as_view()
         ),
    path('methods',
         PaymentMethodView.as_view()
         ),


]
