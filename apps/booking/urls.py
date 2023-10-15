from django.urls import path
from apps.booking import views
urlpatterns = [
    path('user/<int:user_id>/create',
         views.CreateBookingView.as_view(),
         name='availability'
         ),
]
