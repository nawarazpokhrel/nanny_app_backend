from django.urls import path
from apps.booking import views

urlpatterns = [
    path('user/<int:user_id>/create',
         views.CreateBookingView.as_view(),
         name='availability'
         ),
    path('list/booking',
         views.ListBookingView.as_view(),
         name='list-booking'
         ),
    path('<int:booking_id>/accept',
         views.AcceptBookingView.as_view(),
         name='accept-booking'
         ),
    path('search',
         views.SearchUserProfile.as_view(),
         name='accept-booking'
         ),
]
