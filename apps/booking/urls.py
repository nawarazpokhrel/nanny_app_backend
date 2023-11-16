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
    # path('list/booking',
    #      views.ListBookingView.as_view(),
    #      name='list-booking'
    #      ),
    path('<int:booking_id>/accept-reject',
         views.AcceptBookingView.as_view(),
         name='accept-booking'
         ),
    path('history',
         views.ListBookingHistoryView.as_view(),
         name='accept-booking'
         ),
    path('<int:booking_id>/review-add',
         views.AddReviewView.as_view(),
         name='add-review'
         ),
    path('review/list',
         views.ListMyReviewView.as_view(),
         name='list-review'
         ),
]
